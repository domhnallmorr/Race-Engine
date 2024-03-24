import random

def gen_race_start_message():
	messages = [
		"Lights out and away we go!",
		"The race has begun.",
		"And they're off.",
		"The cars are now in motion.",
		"The Grand Prix has started.",
		"Engines roar as the race gets underway.",
		"The race is now in progress.",
		"And so it begins.",
		"The drivers have taken off.",
		"The race has commenced.",
		"And we're racing.",
		"And they're off! The Grand Prix has commenced!",
	]

	return random.choice(messages)

def gen_practice_start_message():
	messages = [
		"Free Practice has begun!",
		"Green light at the end of the pit lane, Practice is underway!",
	]

	return random.choice(messages)

def gen_race_over_message(winning_driver):

	messages = [		
		"And that's the checkered flag! The race is over.",
		f"The race has concluded with {winning_driver} taking the win!",
		f"And it's all over! {winning_driver} crosses the finish line first!",
		"Checkered flag waves as the race comes to an end.",
		f"The Grand Prix has ended, with {winning_driver} emerging victorious!",
		"And there it is! The race is finished, what a thrilling conclusion!",
		"The final lap is complete, marking the end of an exciting race!",
		"The chequered flag drops, sealing the fate of the competitors.",
		"And with that, the race draws to a close. What a spectacle it has been!",
		"The tension dissipates as the race reaches its conclusion. What a race!",
	]

	return random.choice(messages)

def gen_overtake_message(driver_a, driver_b):
	messages = [
		f"And there's the pass! {driver_a} takes the inside line and muscles past {driver_b} for position!",
		f"{driver_a} with a bold move! A late lunge down the outside sees them snatch the place from {driver_b}!",
		f"Patient work from {driver_a} pays off! They close the gap on {driver_b} and make the pass stick!",
		f"{driver_a} makes a daring overtake! A risky maneuver, but it's come off perfectly!",
		f"Textbook move from {driver_a}! They time the pass to perfection and leave {driver_b} with no answer.",
	]

	return random.choice(messages)

def gen_attacking_message(driver_a, driver_b):
	messages = [
		f"{driver_a} really pressursing {driver_b} now!"
	]

	return random.choice(messages)

def gen_retirement_message(driver):
	messages = [ 
		f"{driver} has retired from the race due to mechanical issues.",
		f"Heartbreak for {driver} as they are forced to retire from the race.",
		f"The race ends early for {driver} with a retirement due to technical problems.",
		f"{driver} pulls into the pits and retires from the race.",
		f"Disappointment for {driver} as they're forced to abandon the race.",
		f"Mechanical gremlins strike {driver}, forcing an early retirement.",
		f"{driver} exits the race prematurely due to engine troubles.",
		f"It's game over for {driver} as they retire from the race.",
		f"A tough break for {driver} as they're forced to end their race early.",
		f"{driver} walks away from the car, retiring from the race.",
	]
 
	return random.choice(messages)

def gen_lead_after_turn1_message(driver):
	messages = [ 
		f"{driver} leads the field out of turn 1!"
	]
	
	return random.choice(messages)

def gen_leaving_pit_lane_message(driver):
	messages = [ 
		f"{driver} heading out on track!"
	]
	
	return random.choice(messages)