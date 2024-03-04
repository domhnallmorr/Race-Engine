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
				
			self.laptime = self.base_laptime + random.randint(0, 700) + self.car_model.fuel_effect + self.car_model.tyre_wear + dirty_air_effect

			if self.current_lap == self.pit1_lap:
				self.status = "pitting in"

			if "pitting in" in self.status:
				self.laptime += self.circuit_model.pit_stop_loss
				self.pitstop_times.append(random.randint(3_800, 6_000))
				self.laptime += self.pitstop_times[-1] 
				self.number_of_pitstops += 1

	def complete_lap(self):
		self.laptimes.append(self.laptime)
		self.total_time += self.laptime

		self.car_model.update_fuel(self.circuit_model)

		new_tyres = False
		if self.current_lap == self.pit1_lap:
			new_tyres = True
			
		self.car_model.update_tyre_wear(self.circuit_model, new_tyres)

		self.current_lap += 1



	def recalculate_laptime_when_passed(self, revised_laptime):
		self.total_time -= self.laptimes[-1]
		self.total_time += revised_laptime
		self.laptime = revised_laptime
		self.laptimes[-1] = revised_laptime
		
	def calculate_pitstop_laps(self):
		self.pit1_lap = random.randint(19, 32)

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
