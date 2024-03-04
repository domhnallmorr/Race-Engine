import copy
import threading

from race_engine_model import race_engine_model
from race_engine_view import race_engine_view

class RaceEngineController:
	def __init__(self, app):
		self.app = app

		self.model = race_engine_model.RaceEngineModel()
		self.view = race_engine_view.RaceEngineView(self, self.model.driver_names)

		self.update_timing_screen()

	def update_timing_screen(self):
		self.view.timing_screen.table.update(self.model.standings_df, None)

	def start_race(self):
		self.simulation_thread = threading.Thread(target=self.simulate_race)
		self.simulation_thread.start()
	
	def simulate_race(self):

		if self.model.status == "running" or self.model.status == "pre_race":

			self.model.advance()
			self.view.timing_screen.update_view(self.model.get_data_for_view())
			self.app.after(3000, self.simulate_race)

	def pause_resume(self):
		if self.model.status == "running":
			self.model.status = "paused"
			self.view.timing_screen.start_btn.configure(text="Resume", image=self.view.play_icon2)
		elif self.model.status == "paused":
			self.model.status = "running"
			self.view.timing_screen.start_btn.configure(text="Pause", image=self.view.pause_icon2)
			self.start_race()
			
	def update_commentary(self, commentary):

		if commentary:
			c = commentary.pop(0)
			print(c)
			self.view.timing_screen.update_commentary(f"{c} {len(commentary)}")
			self.app.after(2000, self.update_commentary(commentary))