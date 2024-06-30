import random

from race_engine_model import race_engine_session_model, commentary

class RaceModel(race_engine_session_model.SessionModel):
	def __init__(self, model):
		super().__init__(model)

		self.current_lap = 1
		self.retirements = []

		if "Q1" in self.model.results.keys():
			self.setup_grid_order()

	@property
	def leader(self):
		return self.standings_df.iloc[0]["Driver"]
	
	def setup_grid_order(self):
		qualy_results = self.model.results["Q1"]["results"]
		grid_order = qualy_results["Driver"]

		self.standings_df.set_index('Driver', inplace=True, drop=False)
		self.standings_df = self.standings_df.loc[grid_order]
		self.refresh_standings_column()

	def run_race(self):
		while self.status != "post_race":
			self.advance()

			self.process_headless_commentary()
		self.process_headless_commentary()

	def advance(self):
		if self.status == "pre_session":
			self.commentary_to_process.append(commentary.gen_race_start_message())
			self.calculate_start()
			self.status = "running"

		else: # process lap
			if len(self.commentary_to_process) == 0:
				if self.status == "running":
					self.calculate_lap()
					self.update_fastest_lap()
					self.update_standings()
					self.current_lap += 1
			
					if self.current_lap > self.model.circuit_model.number_of_laps or self.current_lap == 999:
						self.commentary_to_process.append(commentary.gen_race_over_message(self.leader))
						self.status = "post_race"
						# self.log_event("Race Over")

	def calculate_start(self):
		# Calculate Turn 1
		order_after_turn1 = self.calculate_run_to_turn1()

		# redefine particpants based on turn1 order
		self.participants = [o[1] for o in order_after_turn1]

		'''
		just spread field out after turn1
		'''
		for idx, p in enumerate(self.participants):
			p.laptime = self.model.circuit_model.base_laptime + 6_000 + (idx * 1_000) + random.randint(100, 1500)
			p.complete_lap()

		self.update_standings()

		# set fastest lap to leader
		self.fastest_laptime_driver = self.participants[0].name
		self.fastest_laptime = self.participants[0].laptime
		self.fastest_laptime_lap = 1

		self.current_lap += 1


	def calculate_run_to_turn1(self):
		dist_to_turn1 = self.model.circuit_model.dist_to_turn1
		average_speed = 47.0 #m/s

		order_after_turn1 = []
		for idx, p in enumerate([self.model.get_particpant_model_by_name(n) for n in self.standings_df["Driver"].values.tolist()]):
			random_factor = random.randint(-2000, 2000)/1000
			time_to_turn1 = round(dist_to_turn1 / (average_speed + random_factor), 3)
			order_after_turn1.append([time_to_turn1, p])
			
			dist_to_turn1 += 5 # add 5 meters per grid slot

		order_after_turn1 = sorted(order_after_turn1, key=lambda x: x[0], reverse=False)
		'''
		example of order_after_turn1
		[time_to_turn1, particpant model]
		[[12.761, <RaceEngineParticpantModel Mark Webber>], [13.124, <RaceEngineParticpantModel Sebastian Vettel>], [13.68, <RaceEngineParticpantModel Fernando Alonso>],]
		'''

		self.commentary_to_process.append(commentary.gen_lead_after_turn1_message(order_after_turn1[0][1].name))
		
		return order_after_turn1

	def update_standings(self):
		for driver in self.standings_df["Driver"]:
			particpant_model = self.model.get_particpant_model_by_name(driver)
			particpant_model.update_fastest_lap()
			self.standings_df.loc[self.standings_df["Driver"] == driver, "Total Time"] = particpant_model.total_time
			self.standings_df.loc[self.standings_df["Driver"] == driver, "Last Lap"] = particpant_model.laptime
			self.standings_df.loc[self.standings_df["Driver"] == driver, "Lap"] = particpant_model.current_lap
			self.standings_df.loc[self.standings_df["Driver"] == driver, "Status"] = particpant_model.status
	
		self.standings_df = self.standings_df.sort_values(by=["Lap", "Total Time"], ascending=[False, True])
		
		# RESET INDEX AND POSITION COLUMNS
		self.standings_df.reset_index(drop=True, inplace=True)
		self.standings_df["Position"] = self.standings_df.index + 1
		
		# CALC GAP TO CAR IN FRONT
		self.standings_df["Gap Ahead"] = self.standings_df["Total Time"].diff()

		leader_time = self.standings_df.loc[self.standings_df["Position"] == 1, "Total Time"].values[0]
		self.standings_df["Gap to Leader"] = (self.standings_df["Total Time"] - leader_time)

		# UPDATE GAPS TO LEADER IN PARTICIPANT MODEL AND CHECK IF LAPPED
		for idx, row in self.standings_df.iterrows():
			particpant_model = self.model.get_particpant_model_by_name(row["Driver"])	
			particpant_model.positions_by_lap.append(idx + 1)
			particpant_model.gaps_to_leader.append(row["Gap to Leader"])
			
			if row["Gap to Leader"] > self.model.circuit_model.base_laptime:
				self.standings_df.at[idx, "Lapped Status"] = f"lapped {int(row['Gap to Leader']/self.model.circuit_model.base_laptime)}" # add number of laps down to status

			# UPDATE NUMBER OF PITSTOPS
			self.standings_df.at[idx, "Pit"] = particpant_model.number_of_pitstops

			# UPDATE FASTEST LAP
			self.standings_df.at[idx, "Fastest Lap"] = particpant_model.fastest_laptime

		# self.log_event("\nCurrent Standings:\n" + self.standings_df.to_string(index=False))

	def calculate_lap(self):
		'''
		Process
			
			determine driver strategy (push/conserve)
			determine which drivers are fighting for position (within 1s of car in front)
			calculate laptime for each driver, account for dirty air
			determine any mistakes
			determine if overtake if attempted and successfull
			adjust laptimes accordingly
			update standings
			update tyre wear and fuel load
		'''

		for idx, row in self.standings_df.iterrows():
			driver = row["Driver"]
			participant = self.model.get_particpant_model_by_name(driver)

			# ONLY PROCESS IF STILL RUNNING
			if participant.status != "retired":
				# print("not retired")

				gap_ahead = row["Gap Ahead"]
				participant.calculate_laptime(gap_ahead)

				# IF RETIRED THIS LAP
				if participant.status == "retired":
					self.commentary_to_process.append(commentary.gen_retirement_message(participant.name))
					self.retirements.append(participant.name)
					# self.log_event(f"{participant.name} retires")
					laptime_ahead = None

				else:
					if participant.status == "pitting in":
						self.commentary_to_process.append(commentary.gen_entering_pit_lane_message(participant.name))
					
					# print(laptime_ahead)
					if idx > 0 and laptime_ahead is not None: # laptime_ahead being None indicates car in front has retired
						delta = participant.laptime - laptime_ahead
							# self.log_event(f"{participant.name} Pitting In")
						
						if gap_ahead + delta <= 500 and participant_ahead.status not in ["pitting in", "retired"]: # if car ahead is about to pit, don't handle for overtaking
							# self.log_event(f"{driver} Attacking {participant_ahead.name}")
							self.commentary_to_process.append(commentary.gen_attacking_message(driver, participant_ahead.name))

							if random.randint(0, 100) < 25: # overtake successfull
								# self.log_event(f"{participant.name} passes {participant_ahead.name}")
								self.commentary_to_process.append(commentary.gen_overtake_message(participant.name, participant_ahead.name))

								# add some random time to overtaking car, held up when passing
								participant.laptime += random.randint(700, 1_500)

								# recalculate delta due to laptime updated above
								delta = participant.laptime - laptime_ahead 
								
								#update participant that has been passed so laptime brings them behind overtaking car
								orig_gap = gap_ahead + delta
								#if orig_gap >= 0:
								revised_laptime = participant_ahead.laptime + orig_gap + random.randint(700, 1_500)
								participant_ahead.recalculate_laptime_when_passed(revised_laptime)
							else: # overtake unsuccessfull
								participant.laptime = laptime_ahead + random.randint(100, 1_400)
								
					laptime_ahead = participant.laptime
					participant_ahead = participant
					participant.complete_lap()