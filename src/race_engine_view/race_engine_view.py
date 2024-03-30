from tkinter import ttk
from tkinter import *

import customtkinter

from race_engine_view import timing_screen, race_engine_icons, race_weekend_window

class RaceEngineView:
	def __init__(self, controller, driver_names):
		self.controller = controller
		self.driver_names = driver_names

		self.pady = 5
		self.padx = 7
		self.padx_large = 25 # if a large gap is needed

		self.page_title_font = ("Verdana", 30)
		self.header1_font = ("Verdana", 24)
		self.normal_font = ("Verdana", 15)

		self.dark_bg = "#2b2b2b"
		self.light_bg = "#333333"

		race_engine_icons.setup_icons(self)
		self.setup_windows()


	def setup_windows(self):
		self.race_weekend_window = race_weekend_window.RaceWeekendWindow(self.controller.app, self)
		self.race_weekend_window.pack(expand=True, fill=BOTH, side=LEFT)

		self.current_window = self.race_weekend_window

	@staticmethod
	def milliseconds_to_minutes_seconds(milliseconds):
		total_seconds = milliseconds / 1000
		
		# Calculate minutes
		minutes = int(total_seconds // 60)
		
		# Calculate remaining seconds
		seconds = round(total_seconds % 60, 3)
		
		# Calculate remaining milliseconds (fractions of a second)
		remaining_milliseconds = milliseconds % 1000
		
		# format
		time = f"{minutes}.{seconds}"

		return time	
	
	@staticmethod
	def format_seconds(seconds):
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60
    
		return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
	
	def launch_session(self, session):
		self.timing_screen = timing_screen.TimingScreen(self.controller.app, self, session)
		self.race_weekend_window.pack_forget()
		self.timing_screen.pack(expand=True, fill=BOTH, side=LEFT)

		self.current_window = self.timing_screen

	def end_session(self, session, session_result):
		if session == "FP1":
			self.race_weekend_window.disable_go_to_session_btn(session, session_result)
		self.show_window("race_weekend")

	def show_window(self, window):
		self.current_window.pack_forget()

		if window == "race_weekend":
			self.race_weekend_window.pack(expand=True, fill=BOTH, side=LEFT)