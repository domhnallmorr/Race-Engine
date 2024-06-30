from race_engine_model import race_engine_session_model
from race_engine_model import commentary

class TimedSessionModel(race_engine_session_model.SessionModel):
	def __init__(self, model, session_time):
		super().__init__(model)

		self.session_time = session_time
		self.time_left = session_time

		self.setup_session()

	def setup_session(self):

		# SET STAUS COLUMN TO "PIT"
		self.standings_df["Status"] = "PIT"

		# SET PARTICPANTS STATUS
		for participant in self.model.participants:
			participant.status = "in_pits"


	def advance(self):
		if self.status == "pre_session":
			self.status = "running"
			self.commentary_to_process.append(commentary.gen_practice_start_message())
			# self.update_participants_in_practice()
		
		else:
			if len(self.commentary_to_process) == 0:
				if self.status == "running":
					time_delta = 10
					self.find_particpants_leaving_pit_lane()
					self.update_participants_in_practice()

					self.time_left -= time_delta

					# UPDATE STANDINGS
					self.standings_df.sort_values("Fastest Lap", inplace=True)
					self.refresh_standings_column() # in SessionModel

			else: # we have some commentary to process
				if self.model.mode == "headless":
					self.process_lastest_commentary()

		# HANDLE SESSION ENDING
		if self.time_left <= 0:
			self.status = "post_session"

	def find_particpants_leaving_pit_lane(self):
		for p in self.model.participants:
			is_leaving = p.check_leaving_pit_lane(self.time_left)

			if is_leaving is True:
				self.commentary_to_process.append(commentary.gen_leaving_pit_lane_message(p.name))

				# Update standings
				self.standings_df.loc[self.standings_df["Driver"] == p.name, "Status"] = "out_lap"

	def update_participants_in_practice(self):
		participants_running = [p for p in self.model.participants if p.status == "running"]
		for p in self.model.participants:
			if p.status == "running":
				if p.next_update_time > self.time_left:
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Lap"] = p.practice_laps_completed
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Last Lap"] = p.laptime
					self.standings_df.loc[self.standings_df["Driver"] == p.name, "Fastest Lap"] = p.fastest_laptime
					p.update_practice(self.time_left)
				
			# UPDATE STATUS COLUMN FOR ALL
			self.standings_df.loc[self.standings_df["Driver"] == p.name, "Status"] = p.status


	def send_player_car_out(self, driver_name, fuel_load_laps, number_laps_to_run):
		particpant_model = self.model.get_particpant_model_by_name(driver_name)
		particpant_model.send_player_car_out(self.time_left, fuel_load_laps, number_laps_to_run)

	def end_session(self, session):
		fastest_driver = self.standings_df.iloc[0]["Driver"]
		fastest_laptime = self.standings_df.iloc[0]["Fastest Lap"]

		self.model.results[session] = {}
		self.model.results[session]["p1"] = fastest_driver
		self.model.results[session]["fastest lap"] = fastest_laptime
		self.model.results[session]["results"] = self.standings_df.copy(deep=True)