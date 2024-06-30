from race_engine_model import race_engine_timed_session_model

class PracticeModel(race_engine_timed_session_model.TimedSessionModel):
	def __init__(self, model, session_time):
		super().__init__(model, session_time)

		self.generate_practice_runs()

	def generate_practice_runs(self):
		for participant in self.model.participants:
			participant.setup_session()
			if participant not in [self.model.player_driver1, self.model.player_driver2]:
				participant.generate_practice_runs(self.time_left, "FP")
		
	