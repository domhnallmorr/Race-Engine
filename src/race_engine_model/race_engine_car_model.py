

class RaceEngineCarModel:
	def __init__(self, name, speed, color, circuit_model):
		self.name = name
		self.speed = speed
		self.color = color
		self.circuit_model = circuit_model

		self.fuel_load = 155 # kg
		self.tyre_wear = 0 # time lost (in ms) due to tyre wear

	def update_fuel(self, circuit_model):
		self.fuel_load -= circuit_model.fuel_consumption
		self.fuel_load = round(self.fuel_load, 2)

	def update_tyre_wear(self, circuit_model, new_tyres=False):
		if new_tyres is False:
			self.tyre_wear += circuit_model.tyre_wear
		else: # made a pitstop, new tyres fitted
			self.tyre_wear = 0

	@property
	def fuel_effect(self):
		'''
		effect of fuel on lap time
		assume 1kg adds 0.03s to laptime
		'''
		return int(self.fuel_load * 30)

	def calculate_required_fuel(self, number_of_laps):
		number_of_laps = float(number_of_laps) + 0.5 # ensure half a lap of fuel is added for conservatism
		return int(number_of_laps * self.circuit_model.fuel_consumption)

