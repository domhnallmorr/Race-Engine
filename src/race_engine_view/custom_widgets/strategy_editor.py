from tkinter import ttk
from tkinter import *

import customtkinter



class StrategyEditor:
	def __init__(self, parent, view, driver_name, start_col, start_row):
		self.parent = parent
		self.view = view
		self.start_col = start_col
		self.number_laps = 56

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
		for idx in [0, 1, 2]:
			self.setup_edit_widgets(idx, row)
			row += 2

		self.set_default_pit_laps(1)

	def setup_variables(self):
		self.pit1_lap = None
		self.pit2_lap = None
		self.pit3_lap = None

		self.pit1_var = customtkinter.StringVar(value="on")
		self.pit2_var = customtkinter.StringVar(value="off")
		self.pit3_var = customtkinter.StringVar(value="off")

		self.pit_number_vars = [self.pit1_var, self.pit2_var, self.pit3_var]

	def setup_edit_widgets(self, idx, row):
		btn_width = 40

		reduced_pady = 1
		l = customtkinter.CTkLabel(self.parent, text="Some Lap")
		l.grid(row=row, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(self.view.pady, reduced_pady))
		self.lap_labels.append(l)

		m = customtkinter.CTkButton(self.parent, text= "-", width=btn_width, command=lambda idx=idx:self.minus_lap_event(idx))
		m.grid(row=row+1, column=self.start_col + 1, sticky="EW", padx=self.view.padx, pady=(reduced_pady, self.view.pady))
		self.minus_buttons.append(m)

		c = customtkinter.CTkCheckBox(self.parent, text=f"{idx + 1} Stop", variable=self.pit_number_vars[idx], onvalue="on", offvalue="off", width=10,
								command=lambda idx=idx: self.pit_strategy_combo_event(idx))
		c.grid(row=row, column=self.start_col, rowspan=2, sticky="SE", padx=self.view.padx, pady=(reduced_pady, self.view.pady))

		p = customtkinter.CTkProgressBar(self.parent, orientation="horizontal")
		p.grid(row=row+1, column=self.start_col + 2, sticky="EW", padx=self.view.padx, pady=(reduced_pady, self.view.pady))
		self.progress_bars.append(p)

		p = customtkinter.CTkButton(self.parent, text= "+", width=btn_width, command=lambda idx=idx:self.plus_lap_event(idx))
		p.grid(row=row+1, column=self.start_col + 3, sticky="EW", padx=self.view.padx, pady=(reduced_pady, self.view.pady))
		self.plus_buttons.append(p)

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