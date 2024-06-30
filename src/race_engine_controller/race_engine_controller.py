import copy
import threading

from race_engine_model import race_engine_model
from race_engine_view import race_engine_view

class RaceEngineController:
	def __init__(self, app):
		self.app = app

		self.model = race_engine_model.RaceEngineModel("UI")
		self.view = race_engine_view.RaceEngineView(self, self.model.driver_names)

		# self.update_timing_screen()

	def update_timing_screen(self):
		self.view.timing_screen.table.update(self.model.standings_df, None)

	def start_session(self):
		self.simulation_thread = threading.Thread(target=self.simulate_session)
		self.simulation_thread.start()
	
	def simulate_session(self):

		if self.model.current_session.status == "running" or self.model.current_session.status == "pre_session":

			self.model.current_session.advance()
			self.view.timing_screen.update_view(self.model.current_session.get_data_for_view())

			# GET PIT STRATEGY FROM VIEW
			driver1_data = self.view.timing_screen.strategy_editor_driver1.get_data()
			driver2_data = self.view.timing_screen.strategy_editor_driver2.get_data()
			self.model.update_player_drivers_strategy(driver1_data, driver2_data)
			
			self.app.after(1500, self.simulate_session)

			if self.model.current_session.status == "post_session":
				pass #self.view.

	def pause_resume(self):
		if self.model.current_session.status == "running":
			self.model.current_session.status = "paused"
			self.view.timing_screen.start_btn.configure(text="Resume", image=self.view.play_icon2)
		elif self.model.current_session.status == "paused":
			self.model.current_session.status = "running"
			self.view.timing_screen.start_btn.configure(text="Pause", image=self.view.pause_icon2)
			self.start_session()
			
	def update_commentary(self, commentary):

		if commentary:
			c = commentary.pop(0)
			self.view.timing_screen.update_commentary(f"{c} {len(commentary)}")
			self.app.after(2000, self.update_commentary(commentary))

	def go_to_race(self):
		pass

	def go_to_session(self, session):
		if "FP" in session:
			self.model.setup_practice(20*60, session)
		elif "Q" in session:
			self.model.setup_qualfying(60*60, session)
		elif "race" in session:
			self.model.setup_race()

		self.view.launch_session(session)
		self.view.timing_screen.update_view(self.model.current_session.get_data_for_view())

	def end_session(self, session):
		self.model.current_session.end_session(session)
		self.view.end_session(session, self.model.results[session])

	def auto_simulate_session(self, session):
		self.model.simulate_session(session)
		self.end_session(session)

	def send_player_car_out(self, driver_name, fuel_load_laps, number_laps_to_run):
		self.model.current_session.send_player_car_out(driver_name, fuel_load_laps, number_laps_to_run)
