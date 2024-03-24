import random

class RaceEngineParticpantModel:
	def __init__(self, driver, car, circuit, starting_position):
		self.driver = driver
		self.car_model = car
		self.circuit_model = circuit
		self.position = starting_position

		self.current_lap = 1

		self.laptimes = []
		self.gaps_to_leader = []
		self.total_time = 0
		self.pitstop_times = []
		self.positions_by_lap = []
		self.number_of_pitstops = 0

		self.calculate_base_laptime()
		self.calculate_pitstop_laps()
		self.calculate_if_retires()

		self.status = "running"
		self.attacking = False
		self.defending = False

		self.fastest_laptime = None
		self.laptime = None

		self.next_update_time = None # for updating practice session

	def __repr__(self) -> str:
		return f"<RaceEngineParticpantModel {self.driver.name}>"

	@property
	def linestyle(self):
		if self.driver.driver_status == 2:
			return "--"
		else:
			return "-"

	@property
	def name(self):
		return self.driver.name

	def calculate_base_laptime(self):
		self.base_laptime = self.circuit_model.base_laptime

		# add driver component
		'''
		driver with 0 speed rating is considered 3s slower than driver with 100 speed rating
		'''
		self.base_laptime += (100 - self.driver.speed) * 3_0 # 100 * 30 = 3000 (3s in ms)

		# add car component
		'''
		car with 0 speed rating is considered 5s slower than car with 100 speed rating
		'''
		self.base_laptime += (100 - self.car_model.speed) * 5_0

		# print(f"{self.name}: {self.base_laptime}")

	def calculate_laptime(self, gap_ahead):
		# reset status if we just made a pitstop
		if "pitting in" in self.status:
			self.status = "running"

		# CHECK IF RETIRES THIS LAP
		if self.retires is True and self.retire_lap == self.current_lap:
			self.status = "retired"

		# DON'T RETIRE, CALCULATE LAPTIME
		else:
			dirty_air_effect = 0
			if gap_ahead:
				if gap_ahead <= 1_500:
					dirty_air_effect = 500 # assume we lose half a second in dirty air (1.5s or less behind car in front)

			self.calculate_lap_time(700, dirty_air_effect)	

			if self.current_lap in [self.pit1_lap, self.pit2_lap, self.pit3_lap]:
				self.status = "pitting in"

			if "pitting in" in self.status:
				self.laptime += self.circuit_model.pit_stop_loss
				self.pitstop_times.append(random.randint(3_800, 6_000))
				self.laptime += self.pitstop_times[-1] 
				self.number_of_pitstops += 1

	def calculate_lap_time(self, random_element, dirty_air_effect):
		self.laptime = self.base_laptime + random.randint(0, random_element) + self.car_model.fuel_effect + self.car_model.tyre_wear + dirty_air_effect

	def complete_lap(self):
		self.laptimes.append(self.laptime)
		self.total_time += self.laptime

		new_tyres = False
		if self.current_lap == self.pit1_lap:
			new_tyres = True
			
		self.update_fuel_and_tyre_wear()
		self.current_lap += 1

	def update_fuel_and_tyre_wear(self, new_tyres=False):
		self.car_model.update_fuel(self.circuit_model)
		self.car_model.update_tyre_wear(self.circuit_model, new_tyres)

	def recalculate_laptime_when_passed(self, revised_laptime):
		self.total_time -= self.laptimes[-1]
		self.total_time += revised_laptime
		self.laptime = revised_laptime
		self.laptimes[-1] = revised_laptime
		
	def calculate_pitstop_laps(self):
		self.pit1_lap = random.randint(19, 32)
		self.pit2_lap = None
		self.pit3_lap = None

	def calculate_if_retires(self):
		self.retires = False
		self.retire_lap = None

		if random.randint(0, 100) < 20:
			self.retires = True
			self.retire_lap = random.randint(2, self.circuit_model.number_of_laps)

	def update_fastest_lap(self):
		if self.fastest_laptime is None:
			self.fastest_laptime = self.laptime
		elif min(self.laptimes) == self.laptime:
			self.fastest_laptime = self.laptime

	def update_player_pitstop_laps(self, data):
		'''
		data is a dict optained from the view
		{
		"pit1_lap": 24,
		"pit2_lap": ... etc
		}
		'''
		self.pit1_lap = data["pit1_lap"]
		self.pit2_lap = data["pit2_lap"]
		self.pit3_lap = data["pit3_lap"]

	def generate_practice_runs(self, session_time):
		self.practice_laps_completed = 0
		self.practice_runs = [] # [[time_left, fuel, number_laps]]

		time_left = session_time

		while time_left > 0:
			leave_time = random.randint(time_left - (20*60), time_left)
			number_laps = random.randint(3, 14)
			min_fuel_load = int(self.circuit_model.fuel_consumption * number_laps) + 1
			fuel_load = random.randint(min_fuel_load, 155)

			self.practice_runs.append([leave_time, fuel_load, number_laps])

			base_laptime_seconds = self.circuit_model.base_laptime / 1000
			time_left -= number_laps * (base_laptime_seconds + 10)
			time_left -= 10*60 # ensure at least 10 mins spent in pits

	def check_leaving_pit_lane(self, time_left):
		leaving = False

		if len(self.practice_runs) > 0:
			for run in self.practice_runs:
				if run[0] >= time_left:
					leaving = True
					self.pit_in_lap = self.practice_laps_completed + run[2]
					break
		
		if leaving is True:
			self.car_model.tyre_wear = 0
			self.car_model.fuel_load = self.practice_runs[0][1]
			self.practice_runs.pop(0)

			self.update_next_update_time(time_left)
			self.status = "running"
			self.laptime = 120_000 # outlap time

		return leaving
	
	def update_practice(self, time_left):
		self.update_fuel_and_tyre_wear()
		
		if self.practice_laps_completed == self.pit_in_lap:
			self.status = "in_pit"
		else:
			self.practice_laps_completed += 1
			self.calculate_lap_time(700, 0)

			if self.practice_laps_completed == self.pit_in_lap:
				self.laptime += 6_000 # make in lap slow
				
			if self.fastest_laptime is None:
				self.fastest_laptime = self.laptime
			else:
				if self.laptime < self.fastest_laptime:
					self.fastest_laptime = self.laptime
				
			self.update_next_update_time(time_left)

	def update_next_update_time(self, time_left):
		self.next_update_time = time_left - 90