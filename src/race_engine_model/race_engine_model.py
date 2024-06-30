import random

from race_engine_model import race_engine_circuit_model, race_engine_particpant_model, race_engine_car_model, race_engine_driver_model
from race_engine_model import race_engine_practice_model, race_engine_qualy_model, race_engine_race_model

class RaceEngineModel:
	def __init__(self, mode):
		assert mode in ["UI", "headless"], f"Unsupported Mode {mode}" # headless is model only, UI means were using the GUI

		self.mode = mode
		self.circuit_model = race_engine_circuit_model.RaceEngineCircuitModel("Sepang", 56, 93_000)
		self.setup_participants()

		self.results = {}

		self.player_driver1 = self.get_particpant_model_by_name("Nico Rosberg")
		self.player_driver2 = self.get_particpant_model_by_name("Michael Schumacher")

	def setup_participants(self):
		roster_file = r"C:\Users\domhn\Documents\python\race_engine\Race-Engine\src\roster.txt"
		with open(roster_file) as f:
			data = f.readlines()

		self.participants = []
		driver_count = 0

		for line in data:
			line = line.replace("\n", "")

			if line.lower().startswith("team:"):
				line = line.split(":")[1].split(",")
				team_name = line[0].strip()
				max_team_speed = int(line[1])
				min_team_speed = int(line[2])
				team_speed = random.randint(min_team_speed, max_team_speed)
				color = line[3].strip()

			elif line.lower().startswith("driver"):
				if line.lower().startswith("driver1"):
					driver_status = 1
				else:
					driver_status = 2

				line = line.split(":")[1].split(",")
				driver_name = line[0].lstrip().rstrip()
				max_driver_speed = int(line[1])
				min_driver_speed = int(line[2])

				driver_speed = random.randint(min_driver_speed, max_driver_speed)
				driver_count += 1

				car = race_engine_car_model.RaceEngineCarModel(team_name, team_speed, color, self.circuit_model)
				driver = race_engine_driver_model.RaceEngineDriverModel(driver_name, driver_speed, driver_status)
				self.participants.append(race_engine_particpant_model.RaceEngineParticpantModel(driver, car, self.circuit_model, driver_count))

		self.driver_names = [p.driver.name for p in self.participants]
		
	def get_particpant_model_by_name(self, name):
		for p in self.participants:
			if p.name == name:
				return p
			
	def setup_practice(self, session_time, session_name):
		self.current_session = race_engine_practice_model.PracticeModel(self, session_time)
		self.setup_session()

	def setup_qualfying(self, session_time, session_name):
		self.current_session = race_engine_qualy_model.QualyModel(self, session_time)
		self.setup_session()

	def setup_race(self):
		self.current_session = race_engine_race_model.RaceModel(self)
		self.setup_session()

	def setup_session(self):
		for p in self.participants:
			p.setup_variables_for_session()

	def update_player_drivers_strategy(self, driver1_data, driver2_data):
		self.player_driver1.update_player_pitstop_laps(driver1_data)
		self.player_driver2.update_player_pitstop_laps(driver2_data)