import copy
import threading

from race_engine_model import race_engine_model
from race_engine_view import race_engine_view

class RaceEngineController:
	def __init__(self, app):
		self.app = app

		self.model = race_engine_model.RaceEngineModel()
		self.view = race_engine_view.RaceEngineView(self, self.model.driver_names)

		# self.update_timing_screen()

	def update_timing_screen(self):
		self.view.timing_screen.table.update(self.model.standings_df, None)

	def start_session(self):
		self.simulation_thread = threading.Thread(target=self.simulate_session)
		self.simulation_thread.start()
	
	def simulate_session(self):

		if self.model.status == "running" or self.model.status == "pre_session":

			self.model.advance()
			self.view.timing_screen.update_view(self.model.get_data_for_view())

			# GET PIT STRATEGY FROM VIEW
			driver1_data = self.view.timing_screen.strategy_editor_driver1.get_data()
			driver2_data = self.view.timing_screen.strategy_editor_driver2.get_data()
			self.model.update_player_drivers_strategy(driver1_data, driver2_data)
			
			self.app.after(3000, self.simulate_session)

			if self.model.status == "post_session":
				self.

	def pause_resume(self):
		if self.model.status == "running":
			self.model.status = "paused"
			self.view.timing_screen.start_btn.configure(text="Resume", image=self.view.play_icon2)
		elif self.model.status == "paused":
			self.model.status = "running"
			self.view.timing_screen.start_btn.configure(text="Pause", image=self.view.pause_icon2)
			self.start_session()
			
	def update_commentary(self, commentary):

		if commentary:
			c = commentary.pop(0)
			print(c)
			self.view.timing_screen.update_commentary(f"{c} {len(commentary)}")
			self.app.after(2000, self.update_commentary(commentary))

	def go_to_race(self):
		pass

	def go_to_session(self, session):

		self.model.setup_session(session)
		self.view.launch_session(session)
		self.view.timing_screen.update_view(self.model.get_data_for_view())