import copy
import logging
import random

import numpy as np
import pandas as pd

from race_engine_model import race_engine_circuit_model, race_engine_particpant_model, race_engine_car_model, race_engine_driver_model
from race_engine_model import race_engine_model
from race_engine_model import commentary

class RaceEngineModel:
	def __init__(self):
		
		self.circuit_model = race_engine_circuit_model.RaceEngineCircuitModel("Sepang", 56, 93_000)
		self.setup_participants()

		logging.basicConfig(level=logging.INFO, format="%(message)s",
					   handlers=[
                        logging.StreamHandler(),  # Logs to terminal
                        logging.FileHandler("race.log", mode='w')
						]
						)

		# self.setup_standings()

		self.current_lap = 1
		self.time_left = None
		self.status = "pre_session"
		self.fastest_laptime = None
		self.fastest_laptime_driver = None
		self.fastest_laptime_lap = None

		self.commentary_messages = []
		self.commentary_to_process = []

		self.retirements = []
		self.cars_on_track = [] # for practice and qualy

		self.player_driver1 = self.get_particpant_model_by_name("Nico Rosberg")
		self.player_driver2 = self.get_particpant_model_by_name("Michael Schumacher")

		self.results = {} # {"FP1": {"p1": "Vettel"}}

	def log_event(self, event):
		logging.info(f"Lap {self.current_lap}: {event}")

	@property
	def number_cars_on_track(self):
		return len(self.cars_on_track)
	
	@property
	def drivers(self):
		return [p.driver for p in self.participants]
		
	@property
	def driver_names(self):
		return [p.driver.name for p in self.participants]
		
	@property
	def leader(self):
		return self.standings_df.iloc[0]["Driver"]

	def setup_participants(self):

		roster_file = "roster.txt"
		with open(roster_file) as f:
			data = f.readlines()

		self.participants = []
		driver_count = 0

		for line in data:
			line = line.replace("\n", "")

			if line.lower().startswith("team:"):
				line = line.split(":")[1].split(",")
				team_name = line[0].strip()
				max_team_speed = int(line[1])
				min_team_speed = int(line[2])
				team_speed = random.randint(min_team_speed, max_team_speed)
				color = line[3].strip()

			elif line.lower().startswith("driver"):
				if line.lower().startswith("driver1"):
					driver_status = 1
				else:
					driver_status = 2

				line = line.split(":")[1].split(",")
				driver_name = line[0].lstrip().rstrip()
				max_driver_speed = int(line[1])
				min_driver_speed = int(line[2])

				driver_speed = random.randint(min_driver_speed, max_driver_speed)
				driver_count += 1

				car = race_engine_car_model.RaceEngineCarModel(team_name, team_speed, color, self.circuit_model)
				driver = race_engine_driver_model.RaceEngineDriverModel(driver_name, driver_speed, driver_status)
				self.participants.append(race_engine_particpant_model.RaceEngineParticpantModel(driver, car, self.circuit_model, driver_count))

	def get_particpant_model_by_name(self, name):
		for p in self.participants:
			if p.name == name:
				return p
			
	def setup_standings(self):
		'''
		setup pandas dataframe to track standings, assumes participants have been supplied in starting grid order!
		'''
		columns = ["Position", "Driver", "Team", "Lap", "Total Time", "Gap Ahead", "Gap to Leader", "Last Lap", "Status", "Lapped Status", "Pit", "Fastest Lap"] # all times in milliseconds

		data = []
		for participant in self.participants: 
			data.append([participant.position, participant.name, "", 0, 0, 0, 0, "-", "running", None, 0, None])

		self.standings_df = pd.DataFrame(columns=columns, data=data)

		# SETUP STARTING GRID FOR RACE
		if "Q1" in self.results.keys():
			self.standings_df["Driver"] = self.results["Q1"]["results"]["Driver"]

	def run_race(self):
		self.calculate_start()

		while True:
			self.calculate_lap()
			self.update_standings()
			self.current_lap += 1

			if self.current_lap > self.circuit_model.number_of_laps or self.current_lap == 999:
				break

		self.log_event("Race Over")
		print(self.standings_df)

	def advance(self):
		if self.session == "race":
			self.advance_race()
		elif self.session in ["FP1", "Q1"]:
			self.advance_practice()

	def advance_race(self):
		if self.status == "pre_session":
			self.commentary_to_process.append(commentary.gen_race_start_message())
			self.calculate_start()
			self.status = "running"

		else:
			if len(self.commentary_to_process) == 0:
				if self.status == "running":
					self.calculate_lap()
					self.update_fastest_lap()
					self.update_standings()

					self.current_lap += 1
					if self.current_lap > self.circuit_model.number_of_laps or self.current_lap == 999:
						self.commentary_to_process.append(commentary.gen_race_over_message(self.leader))
						self.status = "post_race"
						self.log_event("Race Over")

				for c in self.commentary_to_process:
					self.commentary_messages.append(c)


	def advance_practice(self):
		if self.status == "pre_session":
			self.status = "running"
			self.commentary_to_process.append(commentary.gen_practice_start_message())
			
		else:
			if len(self.commentary_to_process) == 0:
				if self.status == "running":
					
					time_delta = 10
					self.find_particpants_leaving_pit_lane()
					self.update_participants_in_practice()

					self.time_left -= time_delta
					
					# UPDATE STANDINGS
					self.standings_df.sort_values("Fastest Lap", inplace=True)
					self.standings_df.reset_index(drop=True, inplace=True)
					self.standings_df["Position"] = self.standings_df.index + 1

					# Update gaps and intervals
					leader_time = self.standings_df.loc[self.standings_df["Position"] == 1, "Fastest Lap"].values[0]
					laptime_ahead = leader_time

					if leader_time is None:
						self.standings_df["Gap to Leader"] = "-"
						self.standings_df["Gap Ahead"] = "-"
					else:
						gaps = []
						intervals = []
						for idx, row in self.standings_df.iterrows():
							if row["Fastest Lap"] is None:
								gaps.append("-")
							else:
								gaps.append(row["Fastest Lap"] - leader_time)

							if laptime_ahead != "-" and row["Fastest Lap"] is not None:
								intervals.append(row["Fastest Lap"] - laptime_ahead)
							else:
								intervals.append("-")

							laptime_ahead = row["Fastest Lap"]

						self.standings_df["Gap to Leader"] = gaps
						self.standings_df["Gap Ahead"] = intervals

					if self.time_left <= 0.0:
						self.status = "post_session"
						
	def find_particpants_leaving_pit_lane(self):
		for p in self.participants:
			is_leaving = p.check_leaving_pit_lane(self.time_left)

			if is_leaving is True:
				self.commentary_to_process.append(commentary.gen_leaving_pit_lane_message(p.name))

				self.standings_df.loc[self.standings_df["Driver"] == p.name, "Status"] = "out_lap"

	def update_participants_in_practice(self):
		participants_running = [p for p in self.participants if p.status == "running"]
		for p in self.participants:
			if p.status == "running":
				if p.next_update_time > self.time_left:
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Lap"] = p.practice_laps_completed
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Last Lap"] = p.laptime
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Fastest Lap"] = p.fastest_laptime
					p.update_practice(self.time_left)
				
			# UPDATE STATUS COLUMN FOR ALL
			self.standings_df.loc[self.standings_df["Driver"] == p.name, "Status"] = p.status

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
			participant = self.get_particpant_model_by_name(driver)

			# ONLY PROCESS IF STILL RUNNING
			if participant.status != "retired":

				gap_ahead = row["Gap Ahead"]
				participant.calculate_laptime(gap_ahead)

				# IF RETIRED THIS LAP
				if participant.status == "retired":
					self.commentary_to_process.append(commentary.gen_retirement_message(participant.name))
					self.retirements.append(participant.name)
					self.log_event(f"{participant.name} retires")
					laptime_ahead = None

				else:
					if participant.status == "pitting in":
						self.log_event(f"{participant.name} Pitting In")
					
					if idx > 0 and laptime_ahead is not None: # laptime_ahead being None indicates car in front has retired
						delta = participant.laptime - laptime_ahead

						if gap_ahead + delta <= 500 and participant_ahead.status not in ["pitting in", "retired"]: # if car ahead is about to pit, don't handle for overtaking
							
							self.log_event(f"{driver} Attacking {participant_ahead.name}")
							self.commentary_to_process.append(commentary.gen_attacking_message(driver, participant_ahead.name))

							if random.randint(0, 100) < 25: # overtake successfull
								self.log_event(f"{participant.name} passes {participant_ahead.name}")
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

	def calculate_start(self):
		# Calculate Turn 1
		order_after_turn1 = self.calculate_run_to_turn1()

		# redefine particpants based on turn1 order
		self.participants = [o[1] for o in order_after_turn1]

		'''
		just spread field out after turn1
		'''
		for idx, p in enumerate(self.participants):
			p.laptime = self.circuit_model.base_laptime + 6_000 + (idx * 1_000) + random.randint(100, 1500)
			p.complete_lap()

		self.update_standings()

		# set fastest lap to leader
		self.fastest_laptime_driver = self.participants[0].name
		self.fastest_laptime = self.participants[0].laptime
		self.fastest_laptime_lap = 1

		self.current_lap += 1

	def calculate_run_to_turn1(self):
		dist_to_turn1 = self.circuit_model.dist_to_turn1
		average_speed = 47.0 #m/s

		order_after_turn1 = []
		for idx, p in enumerate([self.get_particpant_model_by_name(n) for n in self.standings_df["Driver"].values.tolist()]):
			random_factor = random.randint(-2000, 2000)/1000
			time_to_turn1 = round(dist_to_turn1 / (average_speed + random_factor), 3)
			order_after_turn1.append([time_to_turn1, p])
			
			dist_to_turn1 += 5 # add 5 meters per grid slot

		order_after_turn1 = sorted(order_after_turn1, key=lambda x: x[0], reverse=False)

		self.commentary_to_process.append(commentary.gen_lead_after_turn1_message(order_after_turn1[0][1].name))
		
		return order_after_turn1

	def update_standings(self):
		for driver in self.standings_df["Driver"]:
			particpant_model = self.get_particpant_model_by_name(driver)
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
			particpant_model = self.get_particpant_model_by_name(row["Driver"])	
			particpant_model.positions_by_lap.append(idx + 1)
			particpant_model.gaps_to_leader.append(row["Gap to Leader"])
			
			if row["Gap to Leader"] > self.circuit_model.base_laptime:
				self.standings_df.at[idx, "Lapped Status"] = f"lapped {int(row['Gap to Leader']/self.circuit_model.base_laptime)}" # add number of laps down to status

			# UPDATE NUMBER OF PITSTOPS
			self.standings_df.at[idx, "Pit"] = particpant_model.number_of_pitstops

			# UPDATE FASTEST LAP
			self.standings_df.at[idx, "Fastest Lap"] = particpant_model.fastest_laptime

		self.log_event("\nCurrent Standings:\n" + self.standings_df.to_string(index=False))

	def update_fastest_lap(self):
		for driver in self.standings_df["Driver"]:
			particpant_model = self.get_particpant_model_by_name(driver)
			if particpant_model.laptime < self.fastest_laptime:
				self.fastest_laptime = particpant_model.laptime
				self.fastest_laptime_driver = driver
				self.fastest_laptime_lap = self.current_lap

	def get_data_for_view(self):
		data = {}

		data["status"] = self.status
		data["current_lap"] = self.current_lap
		data["total_laps"] = self.circuit_model.number_of_laps
		data["time_left"] = self.time_left
		data["standings"] = self.standings_df.copy(deep=True)
		
		data["fastest_lap_times"] = [p.name for p in self.participants if p.fastest_laptime == p.laptime]
		data["fastest_laptime"] = self.fastest_laptime
		data["fastest_laptime_driver"] = self.fastest_laptime_driver

		data["retirements"] = self.retirements

		if len(self.commentary_to_process) > 0:
			data["commentary"] = self.commentary_to_process.pop(0)
		else:
			data["commentary"] = ""

		# HACK FOR NOW
		driver1 = self.get_particpant_model_by_name("Nico Rosberg")
		data["driver1_fuel"] = driver1.car_model.fuel_load

		# LAP TIMES DATA
		data["laptimes"] = {}
		for p in self.participants:
			data["laptimes"][p.name] = copy.deepcopy(p.laptimes)

		return data
	
	def update_player_drivers_strategy(self, driver1_data, driver2_data):
		self.player_driver1.update_player_pitstop_laps(driver1_data)
		self.player_driver2.update_player_pitstop_laps(driver2_data)
		
	def setup_session(self, session):
		self.session = session
		self.status = "pre_session"

		self.setup_standings()

		if session in ["FP1", "Q1"]:
			if session == "FP1":
				self.time_left = 120 * 60  # 2 hours in seconds
			elif session == "Q1":
				self.time_left = 60 * 60 # 1hr qualy session

			for participant in self.participants:
				participant.setup_session()
				if participant not in [self.player_driver1, self.player_driver2]:
					participant.generate_practice_runs(self.time_left, session)
				participant.status = "in_pits"

			# SET STAUS COLUMN TO "PIT"
			self.standings_df["Status"] = "PIT"

		
		elif session == "race":
			for participant in self.participants:
				participant.status = "running"

	def end_session(self, session):
		fastest_driver = self.standings_df.iloc[0]["Driver"]
		fastest_laptime = self.standings_df.iloc[0]["Fastest Lap"]

		self.results[session] = {}
		self.results[session]["p1"] = fastest_driver
		self.results[session]["fastest lap"] = fastest_laptime
		self.results[session]["results"] = self.standings_df.copy(deep=True)

	def simulate_session(self, session):
		self.setup_session(session)

		while self.status != "post_session":
			self.advance()
			if len(self.commentary_to_process) > 0:
				self.commentary_to_process.pop(0)

	def send_player_car_out(self, driver_name, fuel_load_laps, number_laps_to_run):
		particpant_model = self.get_particpant_model_by_name(driver_name)
		particpant_model.send_player_car_out(self.time_left, fuel_load_laps, number_laps_to_run)
