
from tkinter import ttk
from tkinter import *

import customtkinter

from race_engine_view import timing_screen

class RaceEngineView:
	def __init__(self, controller, driver_names):
		self.controller = controller
		self.driver_names = driver_names

		self.pady = 5
		self.padx = 7
		self.padx_large = 25 # if a large gap is needed

		self.header1_font = ("Verdana", 24)

		self.dark_bg = "#2b2b2b"
		self.light_bg = "#333333"
		self.setup_windows()


	def setup_windows(self):
		self.timing_screen = timing_screen.TimingScreen(self.controller.app, self)
		self.timing_screen.pack(expand=True, fill=BOTH, side=LEFT)

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