
from race_engine_model import race_engine_model

for i in range(100):
	model = race_engine_model.RaceEngineModel("headless")
	# model.setup_practice(60 * 60, "FP1")

	# model.current_session.advance()

	# while model.current_session.status != "post_session":
	# 	model.current_session.advance()

	# print(model.current_session.standings_df)
	# print(model.current_session.time_left)

	# model.setup_qualfying(60 * 60, "Qualfying")

	# model.current_session.advance()

	# while model.current_session.status != "post_session":
	# 	model.current_session.advance()

	# print(model.current_session.standings_df)
	# print(model.current_session.time_left)

	model.setup_race()
	model.current_session.run_race()