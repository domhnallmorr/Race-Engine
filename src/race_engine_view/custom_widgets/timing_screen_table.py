from tksheet import Sheet

class TimingScreenTable(Sheet):
	def __init__(self, parent, view):
		self.view = view
		self.headers = ["Name", "Gap", "Interval", "Last Lap"]
		
		super().__init__(parent, headers=self.headers)


		# STYLING
		self.set_options(table_bg="#333333")
		self.set_options(header_bg="#333333")
		self.set_options(index_bg="#333333")
		self.set_options(top_left_bg="#333333")
		
		self.set_options(table_fg="white")
		self.set_options(header_fg="white")
		self.set_options(index_fg="white")

		# self.set_options(auto_resize_columns=True)
	def set_column_widths(self):
		self.column_width(column=0, width=300, only_set_if_too_small=False, redraw=True)
		self.column_width(column=1, width=100, only_set_if_too_small=False, redraw=True)
		self.column_width(column=2, width=100, only_set_if_too_small=False, redraw=True)
		self.column_width(column=3, width=100, only_set_if_too_small=False, redraw=True)

	def update(self, standings_df, fastest_lap_times=[], retirements=[]):
		data = []

		for idx, row in standings_df.iterrows():
			if row["Status"] == "retired":
				last_lap = "STOP"
			else:
				last_lap = self.view.milliseconds_to_minutes_seconds(row["Last Lap"])
			
			if idx == 0:
				interval = row["Lap"]
				gap = "Lap"
			elif row["Status"] == "retired":
				interval = ""
				gap = ""
			else:
				interval = row["Gap Ahead"]/1000
				if row["Lapped Status"] == "lapped":
					gap = "+1"
				else:
					gap = row["Gap to Leader"]/1000
				
			data.append([row["Driver"], gap, f'{interval}', last_lap])

		self.set_sheet_data(data, redraw=False) # redraw=False to avoid flickering of table in view

		lap_col_idx = 3
		# highlight fastest laps
		for idx, driver in enumerate(standings_df["Driver"].values.tolist()):
			self.highlight_cells(row=idx, column=1, fg="#f0e511") # make gap column yellow

			if driver in fastest_lap_times:
				self.highlight_cells(row=idx, column=lap_col_idx, fg="#54d426")
			else:
				self.highlight_cells(row=idx, column=lap_col_idx, fg="white")

			if driver in retirements:
				self.highlight_cells(row=idx, column=lap_col_idx, fg="#eb4034")			
			
		self.set_column_widths() # Table redrawn here

	
