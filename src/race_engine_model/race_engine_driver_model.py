

class RaceEngineDriverModel:
	def __init__(self, name, speed, driver_status):
		self.name = name
		self.speed = speed
		self.driver_status = driver_status

	def __repr__(self) -> str:
		return f"<RaceEngineDriverModel {self.name}>"
	
