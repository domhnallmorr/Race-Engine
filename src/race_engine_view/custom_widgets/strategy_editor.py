from tkinter import ttk
from tkinter import *

import customtkinter



class StrategyEditor:
	def __init__(self, parent, view, driver_name, start_col, start_row, session):
		self.parent = parent
		self.view = view
		self.start_col = start_col
		#TODO make circuit specific
		self.number_laps = 56
		self.session = session
		self.driver_name = driver_name

		self.one_third_distance = int(self.number_laps / 3)
		self.half_distance = int(self.number_laps / 2)
		self.two_third_distance = int(2 * (self.number_laps / 3))
		self.one_quarter_distance = int(self.number_laps / 4)
		self.three_quarters_distance = int(3 * (self.number_laps / 4))

		customtkinter.CTkLabel(self.parent, text=driver_name, anchor=W).grid(row=start_row, column=start_col, columnspan=4, padx=self.view.padx, pady=self.view.pady, sticky="EW")

		self.setup_variables()

		self.progress_bars = []
		self.lap_labels = []
		self.minus_buttons = []
		self.plus_buttons = []

		row = start_row + 1

		if self.session in ["FP1"]:
			self.setup_practice_edit_widgets(row)
			self.change_fuel_event(change=None)
			self.change_laps_to_run_event(change=None)
		else: # RACE
			for idx in [0, 1, 2]:
				self.setup_race_edit_widgets(idx, row)
				row += 2

			self.set_default_pit_laps(1)

	def setup_variables(self):
		# PRACTICE VARIABLES
		self.fuel_load_laps = int(self.number_laps / 2) # in laps
		self.number_laps_to_run = 5

		# RACE VARIABLES
		self.pit1_lap = None
		self.pit2_lap = None
		self.pit3_lap = None

		self.pit1_var = customtkinter.StringVar(value="on")
		self.pit2_var = customtkinter.StringVar(value="off")
		self.pit3_var = customtkinter.StringVar(value="off")

		self.pit_number_vars = [self.pit1_var, self.pit2_var, self.pit3_var]

		self.btn_width = 40
		self.reduced_pady = 1

	def setup_race_edit_widgets(self, idx, row):

		l = customtkinter.CTkLabel(self.parent, text="Some Lap")
		l.grid(row=row, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.view.pady, self.reduced_pady))
		self.lap_labels.append(l)

		m = customtkinter.CTkButton(self.parent, text= "-", width=self.btn_width, command=lambda idx=idx:self.minus_lap_event(idx))
		m.grid(row=row+1, column=self.start_col + 1, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))
		self.minus_buttons.append(m)

		c = customtkinter.CTkCheckBox(self.parent, text=f"{idx + 1} Stop", variable=self.pit_number_vars[idx], onvalue="on", offvalue="off", width=10,
								command=lambda idx=idx: self.pit_strategy_combo_event(idx))
		c.grid(row=row, column=self.start_col, rowspan=2, sticky="SE", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		p = customtkinter.CTkProgressBar(self.parent, orientation="horizontal")
		p.grid(row=row+1, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))
		self.progress_bars.append(p)

		p = customtkinter.CTkButton(self.parent, text= "+", width=self.btn_width, command=lambda idx=idx:self.plus_lap_event(idx))
		p.grid(row=row+1, column=self.start_col + 3, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))
		self.plus_buttons.append(p)

	def setup_practice_edit_widgets(self, row):
		# FUEL LOAD
		self.fuel_load_label = customtkinter.CTkLabel(self.parent, text="%")
		self.fuel_load_label.grid(row=row+1, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		customtkinter.CTkLabel(self.parent, text="Fuel Load:").grid(row=row+2, column=self.start_col, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		m = customtkinter.CTkButton(self.parent, text= "-", width=self.btn_width, command=lambda change="minus": self.change_fuel_event(change))
		m.grid(row=row+2, column=self.start_col + 1, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		self.fuel_load_progress_bar = customtkinter.CTkProgressBar(self.parent, orientation="horizontal")
		self.fuel_load_progress_bar.grid(row=row+2, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		p = customtkinter.CTkButton(self.parent, text= "+", width=self.btn_width, command=lambda change="plus": self.change_fuel_event(change))
		p.grid(row=row+2, column=self.start_col + 3, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		# NUMBER OF LAPS TO RUN
		self.number_laps_to_run_label = customtkinter.CTkLabel(self.parent, text="X Laps")
		self.number_laps_to_run_label.grid(row=row+3, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		customtkinter.CTkLabel(self.parent, text="No. Laps To Run:").grid(row=row+4, column=self.start_col, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		m = customtkinter.CTkButton(self.parent, text= "-", width=self.btn_width, command=lambda change="minus": self.change_laps_to_run_event(change))
		m.grid(row=row+4, column=self.start_col + 1, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		self.laps_to_run_progress_bar = customtkinter.CTkProgressBar(self.parent, orientation="horizontal")
		self.laps_to_run_progress_bar.grid(row=row+4, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		p = customtkinter.CTkButton(self.parent, text= "+", width=self.btn_width, command=lambda change="plus": self.change_laps_to_run_event(change))
		p.grid(row=row+4, column=self.start_col + 3, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))

		# SEND OUT BUTTOn
		b = customtkinter.CTkButton(self.parent, text= "Send Out", width=self.btn_width, command=self.send_out)
		b.grid(row=row+5, column=self.start_col, sticky="EW", padx=self.view.padx, pady=(self.reduced_pady, self.view.pady))


	def pit_strategy_combo_event(self, idx_clicked):
		for idx, var in enumerate(self.pit_number_vars):
			if idx == idx_clicked:
				var.set("on")
			else:
				var.set("off")

		self.set_default_pit_laps(idx_clicked + 1)

	def set_default_pit_laps(self, number_of_stops):
		self.update_lap_label(1, None)
		self.update_lap_label(2, None)

		# disable buttons
		self.minus_buttons[1].configure(state="disabled")
		self.minus_buttons[2].configure(state="disabled")

		self.plus_buttons[1].configure(state="disabled")
		self.plus_buttons[2].configure(state="disabled")

		# SET PROGRESS BARS
		self.progress_bars[1].set(0)
		self.progress_bars[2].set(0)

		if number_of_stops == 1:
			self.progress_bars[0].set(0.5)
			self.pit1_lap = self.half_distance
			self.update_lap_label(0, self.pit1_lap)
			
		elif number_of_stops == 2:
			self.progress_bars[0].set(0.33)
			self.pit1_lap = self.one_third_distance
			self.update_lap_label(0, self.pit1_lap)

			self.progress_bars[1].set(0.66)
			self.pit2_lap = self.two_third_distance
			self.update_lap_label(1, self.pit2_lap)
			self.minus_buttons[1].configure(state="normal")
			self.plus_buttons[1].configure(state="normal")

		elif number_of_stops == 3:
			self.progress_bars[0].set(0.25)
			self.pit1_lap = self.one_quarter_distance
			self.update_lap_label(0, self.pit1_lap)

			self.progress_bars[1].set(0.50)	
			self.pit2_lap = self.half_distance
			self.update_lap_label(1, self.pit2_lap)
			self.minus_buttons[1].configure(state="normal")
			self.plus_buttons[1].configure(state="normal")

			self.progress_bars[2].set(0.75)		
			self.pit3_lap = self.three_quarters_distance
			self.update_lap_label(2, self.pit3_lap)	
			self.minus_buttons[2].configure(state="normal")
			self.plus_buttons[2].configure(state="normal")

	def update_lap_label(self, label_idx, pit_lap):
		if pit_lap == None:
			self.lap_labels[label_idx].configure(text="N/A")
		else:
			percentage = int((pit_lap/self.number_laps)*100)
			self.lap_labels[label_idx].configure(text=f"Lap {pit_lap} / {self.number_laps} ({percentage}%)")
			self.progress_bars[label_idx].set(percentage/100)

	def minus_lap_event(self, idx):
		process = True

		# AVOID LAP 1 or BELOW
		if idx == 0 and self.pit1_lap < 3:
			process = False

		# AVOID STOP 2 BEFORE STOP 1
		if idx == 1 and self.pit2_lap - self.pit1_lap == 1:
			process = False

		# AVOID STOP 3 BEFORE STOP 2
		if idx == 2 and self.pit3_lap - self.pit2_lap == 1:
			process = False

		if process is True:
			if idx == 0:
				self.pit1_lap -= 1
				self.update_lap_label(idx, self.pit1_lap)

			elif idx == 1:
				self.pit2_lap -= 1
				self.update_lap_label(idx, self.pit2_lap)

			elif idx == 2:
				self.pit3_lap -= 1
				self.update_lap_label(idx, self.pit3_lap)

	def plus_lap_event(self, idx):
		process = True

		# AVOID LAST 1 or ABOVE
		if idx == 0 and self.pit1_lap == self.number_laps - 1:
			process = False
		
		if idx == 1 and self.pit2_lap == self.number_laps - 1:
			process = False

		if idx == 2 and self.pit3_lap == self.number_laps - 1:
			process = False

		# AVOID STOP 1 AFTTER STOP 2
		if idx == 0 and self.pit2_lap is not None and self.pit2_lap - self.pit1_lap == 1:
			process = False

		# AVOID STOP 2 AFTER STOP 2
		if idx == 1 and self.pit3_lap is not None and self.pit3_lap - self.pit2_lap == 1:
			process = False

		if process is True:
			if idx == 0:
				self.pit1_lap += 1
				self.update_lap_label(idx, self.pit1_lap)

			elif idx == 1:
				self.pit2_lap += 1
				self.update_lap_label(idx, self.pit2_lap)

			elif idx == 2:
				self.pit3_lap += 1
				self.update_lap_label(idx, self.pit3_lap)

	def get_data(self):
		data = {
			"pit1_lap": self.pit1_lap,
			"pit2_lap": self.pit2_lap,
			"pit3_lap": self.pit3_lap,
		}

		return data
	
	def change_fuel_event(self, change):
		if change == "plus" and self.fuel_load_laps < self.number_laps:
			self.fuel_load_laps += 1

		if change == "minus" and self.fuel_load_laps > 2:
			self.fuel_load_laps -= 1

		percentage = int((self.fuel_load_laps / self.number_laps) * 100)
		self.fuel_load_progress_bar.set(percentage/100)

		self.fuel_load_label.configure(text=f"Lap {self.fuel_load_laps} / {self.number_laps} ({percentage}%)")

		# ensure we don't try to run more laps than fuel in car
		if self.fuel_load_laps < self.number_laps_to_run:
			self.number_laps_to_run = self.fuel_load_laps
			self.change_laps_to_run_event(change=None)

	def change_laps_to_run_event(self, change):
		if change == "plus" and self.number_laps_to_run < 15:
			if self.number_laps_to_run + 1 <= self.fuel_load_laps:
				self.number_laps_to_run += 1

		if change == "minus" and self.number_laps_to_run > 3:
			self.number_laps_to_run -= 1

		self.laps_to_run_progress_bar.set(self.number_laps_to_run/15)

		self.number_laps_to_run_label.configure(text=f"{self.number_laps_to_run} Laps")

	def send_out(self):
		self.view.controller.send_player_car_out(self.driver_name, self.fuel_load_laps, self.number_laps_to_run)