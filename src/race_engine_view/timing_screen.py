
from tkinter import ttk
from tkinter import *

import customtkinter

import matplotlib
from matplotlib import style
style.use('dark_background')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from race_engine_view.custom_widgets import timing_screen_table, strategy_editor

class TimingScreen(customtkinter.CTkFrame):
	def __init__(self, master, view, session):
		super().__init__(master)

		self.view = view
		self.session = session

		self.setup_frames()
		self.setup_labels()
		self.setup_buttons()
		self.setup_widgets()
		self.setup_plots()
		self.config_grid()

	def config_grid(self):
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)

		self.top_frame.grid_columnconfigure(4, weight=1)

		self.commentary_frame.grid_columnconfigure(1, weight=1)

		self.button_frame.grid_rowconfigure(10, weight=1)

		self.laptimes_frame.grid_columnconfigure(7, weight=1)
		self.laptimes_frame.grid_rowconfigure(2, weight=1)

		self.player_frame_dummy.grid_columnconfigure(0, weight=1)
		self.player_frame_dummy.grid_rowconfigure(0, weight=1)

		self.player_frame.grid_columnconfigure(0, weight=1)
		self.player_frame.grid_columnconfigure(1, weight=1)

		# note, frames are used as seperators on the strategy frame, these are expanded by the commands below
		self.strategy_frame.grid_columnconfigure(6, weight=1)
		self.strategy_frame.grid_columnconfigure(12, weight=1)
		self.strategy_frame.grid_rowconfigure(10, weight=1)

	def setup_frames(self):
		self.top_frame = customtkinter.CTkFrame(self)
		self.top_frame.grid(row=0, column=0, columnspan=2, sticky="EW", pady=self.view.pady)

		self.commentary_frame = customtkinter.CTkFrame(self)
		self.commentary_frame.grid(row=1, column=0, columnspan=2, sticky="EW", pady=self.view.pady)

		self.button_frame = customtkinter.CTkFrame(self)
		self.button_frame.grid(row=2, column=0, sticky="NSEW", pady=self.view.pady, padx=(0, self.view.padx))

		self.strategy_frame = customtkinter.CTkFrame(self)
		self.strategy_frame.grid(row=2, column=1, sticky="NSEW", pady=self.view.pady, padx=(self.view.padx, 0))

		self.laptimes_frame = customtkinter.CTkFrame(self)
		self.laptimes_frame.grid(row=2, column=1, sticky="NSEW", pady=self.view.pady, padx=(self.view.padx, 0))

		self.timing_frame = customtkinter.CTkFrame(self)
		self.timing_frame.grid(row=2, column=1, sticky="NSEW", pady=self.view.pady, padx=(self.view.padx, 0))

		self.player_frame_dummy = customtkinter.CTkFrame(self)
		self.player_frame_dummy.grid(row=3, column=0, columnspan=2, sticky="EW", pady=self.view.pady)

		self.player_frame = customtkinter.CTkFrame(self.player_frame_dummy)
		self.player_frame.grid(row=0, column=0, sticky="NSEW")

		self.driver1_frame = customtkinter.CTkFrame(self.player_frame)
		self.driver1_frame.grid(row=0, column=0, sticky="NSEW", padx=40)

		self.driver2_frame = customtkinter.CTkFrame(self.player_frame)
		self.driver2_frame.grid(row=0, column=1, sticky="NSEW", padx=40)

	def setup_labels(self):
		self.title_label = customtkinter.CTkLabel(self.top_frame, text="RACE", font=self.view.header1_font)
		self.title_label.grid(row=0, column=0, padx=self.view.padx, pady=self.view.pady, sticky="NW")
		if self.session == "FP1":
			self.title_label.configure(text="Friday Practice")

		self.lap_label = customtkinter.CTkLabel(self.top_frame, text="PRE-RACE", width=100, anchor=W)
		self.lap_label.grid(row=1, column=0, padx=self.view.padx, pady=self.view.pady, sticky="NW")
		if self.session != "race":
			self.lap_label.configure(text="PRE-SESSION")

		self.fastest_laptime_label = customtkinter.CTkLabel(self.top_frame, text="FASTEST LAP: N/A")
		self.fastest_laptime_label.grid(row=1, column=1, padx=self.view.padx, pady=self.view.pady, sticky="NW")

		self.venue_label = customtkinter.CTkLabel(self.top_frame, text="SEPANG INTERNATIONAL CIRCUIT")
		self.venue_label.grid(row=1, column=4, padx=self.view.padx, pady=self.view.pady, sticky="NE")

		self.commentary_label = customtkinter.CTkLabel(self.commentary_frame, text="")
		self.commentary_label.grid(row=1, column=1, padx=self.view.padx, pady=self.view.pady, sticky="EW")


		# driver labels
		customtkinter.CTkLabel(self.driver1_frame, text="Rosberg").grid(row=1, column=1, sticky="EW")
		customtkinter.CTkLabel(self.driver2_frame, text="Schumacher").grid(row=1, column=1, sticky="EW")

		self.driver1_fuel_label = customtkinter.CTkLabel(self.driver1_frame, text="0.0kg")
		self.driver1_fuel_label.grid(row=2, column=1, sticky="EW")

		# LABELS FOR LAPTIMES PLOTS
		customtkinter.CTkLabel(self.laptimes_frame, text="Driver 1", anchor=W).grid(row=0, column=1, sticky="EW", padx=self.view.padx, pady=self.view.pady)
		customtkinter.CTkLabel(self.laptimes_frame, text="Driver 2 (Optional)", anchor=W).grid(row=0, column=3, sticky="EW", padx=self.view.padx, pady=self.view.pady)

	def setup_buttons(self):
		self.timing_button = customtkinter.CTkButton(self.button_frame, text="Timing", command=lambda window="timing": self.show_window(window), image=self.view.timing_icon2,  compound=LEFT, anchor="w")
		self.timing_button.grid(row=0, column=0, sticky="EW", padx=self.view.padx, pady=self.view.pady)

		self.lap_times_button = customtkinter.CTkButton(self.button_frame, text="Lap Times", command=lambda window="laptimes": self.show_window(window), image=self.view.stopwatch_icon2, anchor="w")
		self.lap_times_button.grid(row=1, column=0, sticky="EW", padx=self.view.padx, pady=self.view.pady)

		self.strategy_button = customtkinter.CTkButton(self.button_frame, text="Strategy", command=lambda window="strategy": self.show_window(window), image=self.view.pit_icon2, anchor="w")
		self.strategy_button.grid(row=2, column=0, sticky="EW", padx=self.view.padx, pady=self.view.pady)

		self.start_btn = customtkinter.CTkButton(self.button_frame, text="Start Race", command=self.start_session, image=self.view.play_icon2, anchor="w")
		self.start_btn.grid(row=10, column=0, padx=self.view.padx, pady=self.view.pady, sticky="SEW")
		if self.session != "race":
			self.start_btn.configure(text="Start Session")

	def setup_widgets(self):
		self.table = timing_screen_table.TimingScreenTable(self.timing_frame, self.view, self.session)
		self.table.pack(expand=True, fill=BOTH, side=LEFT)

		combo_width = 300
		# LAP TIMES COMBOS
		self.driver1_laptime_combo = customtkinter.CTkComboBox(self.laptimes_frame, values=self.view.driver_names, command=self.update_laptimes_plot, width=combo_width)
		self.driver1_laptime_combo.grid(row=1, column=1, sticky="EW", padx=self.view.padx, pady=self.view.pady)
		self.driver1_laptime_combo.set("Nico Rosberg")

		self.driver2_laptime_var = customtkinter.StringVar(value="on")
		self.driver2_laptime_checkbox = customtkinter.CTkCheckBox(self.laptimes_frame, text="", variable=self.driver2_laptime_var, onvalue="on", offvalue="off", width=10, command=self.update_laptimes_plot)
		self.driver2_laptime_checkbox.grid(row=1, column=2, sticky="E", padx=(120, 5), pady=self.view.pady)

		self.driver2_laptime_combo = customtkinter.CTkComboBox(self.laptimes_frame, values=self.view.driver_names, command=self.update_laptimes_plot, width=combo_width)
		self.driver2_laptime_combo.grid(row=1, column=3, sticky="EW", padx=(5, 5), pady=self.view.pady)
		self.driver2_laptime_combo.set("Michael Schumacher")

		# STRATEGY CHECKBOXES
		self.driver1_pit1_var = customtkinter.StringVar(value="on")
		self.driver1_pit2_var = customtkinter.StringVar(value="off")
		self.driver1_pit3_var = customtkinter.StringVar(value="off")
		self.driver1_pit_vars = [self.driver1_pit1_var, self.driver1_pit2_var, self.driver1_pit3_var]

		# STRATEGY EDITORS
		self.strategy_editor_driver1 = strategy_editor.StrategyEditor(self.strategy_frame, self.view, "Rosberg", 1, 1)

		# hack to create a seperator
		customtkinter.CTkFrame(self.strategy_frame, width=10).grid(column=6, row=1, rowspan=20, padx=(100, 10), sticky="NSEW")
		self.strategy_editor_driver2 = strategy_editor.StrategyEditor(self.strategy_frame, self.view, "Schumacher", 7, 1)
		customtkinter.CTkFrame(self.strategy_frame, width=10).grid(column=12, row=1, rowspan=20, padx=50, sticky="NSEW")
		
	def setup_plots(self):
		# LAPTIMES
		self.laptimes_figure = Figure(figsize=(5,5), dpi=100)
		self.laptimes_axis = self.laptimes_figure.add_subplot(111)

		self.laptimes_canvas = FigureCanvasTkAgg(self.laptimes_figure, self.laptimes_frame)
		self.laptimes_canvas.draw()
		self.laptimes_canvas.get_tk_widget().grid(row=2, column=0, columnspan=8, pady=2,sticky="nsew")	

	def start_session(self):
		self.start_btn.configure(text="Pause", command=self.view.controller.pause_resume, image=self.view.pause_icon2)
		self.view.controller.start_session()

	def update_view(self, data):

		if self.session == "race":
			if data["current_lap"] > data["total_laps"]:
				self.lap_label.configure(text="RACE OVER")
			else:
				self.lap_label.configure(text=f"LAP {data['current_lap']}/{data['total_laps']}")
		else:
			self.lap_label.configure(text=self.view.format_seconds(data["time_left"]))

		if data["fastest_laptime"] is None:
			fastest_laptime = "-" # no laps set yet
		else:
			fastest_laptime = self.view.milliseconds_to_minutes_seconds(data["fastest_laptime"])
		self.fastest_laptime_label.configure(text=f"FASTEST LAP: {fastest_laptime} ({data['fastest_laptime_driver']})")

		self.table.update(data["standings"], data["fastest_laptime"], data["fastest_lap_times"], data["retirements"])
		
		self.commentary_label.configure(text=data["commentary"])
		self.driver1_fuel_label.configure(text=f'{data["driver1_fuel"]}kg')
		
		self.laptimes_data = data["laptimes"]
		self.update_laptimes_plot()

	def show_window(self, window):
		
		if window == "timing":
			self.timing_frame.tkraise()
		elif window == "laptimes":
			self.laptimes_frame.tkraise()
		elif window == "strategy":
			self.strategy_frame.tkraise()

	def update_laptimes_plot(self, event=None):
		self.laptimes_axis.cla()

		laptimes = self.laptimes_data[self.driver1_laptime_combo.get()]
		laps = [i for i in range(len(laptimes))]
		self.laptimes_axis.plot(laps, laptimes, label=self.driver1_laptime_combo.get())

		if self.driver2_laptime_var.get() == "on":
			laptimes = self.laptimes_data[self.driver2_laptime_combo.get()]
			laps = [i for i in range(len(laptimes))]
			self.laptimes_axis.plot(laps, laptimes, label=self.driver2_laptime_combo.get())

		self.laptimes_axis.set_xlabel("Lap")
		self.laptimes_axis.set_ylabel("Time")
		self.laptimes_axis.legend()
		self.laptimes_axis.grid(alpha=0.5)

		default_y_ticks = self.laptimes_axis.get_yticks()

		self.laptimes_axis.set_yticks(default_y_ticks)
		self.laptimes_axis.set_yticklabels([self.view.milliseconds_to_minutes_seconds(t) for t in default_y_ticks])

		self.laptimes_canvas.draw()


