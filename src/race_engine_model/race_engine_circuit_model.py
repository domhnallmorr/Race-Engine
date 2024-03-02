

class RaceEngineCircuitModel:
	def __init__(self, name, number_of_laps, base_laptime):
		self.name = name
		self.number_of_laps = number_of_laps
		self.base_laptime = base_laptime

		'''
		Assume 155kg required to run race, round down a little for conservatism
		'''
		self.fuel_consumption = round((155/self.number_of_laps) - 0.1, 2)

		'''
		base tyre wear, 20 laps equates to 1 second loss in performance
		'''
		self.tyre_wear = int(1_000 / 20)

		self.pit_stop_loss = 20_000 #20s loss coming through pits

