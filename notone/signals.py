from blinker import signal

game_started = signal("game_started")
game_ended = signal("game_ended")

round_started = signal("round_started")
round_ended = signal("round_ended")

turn_started = signal("turn_started")
turn_ended = signal("turn_ended")

rolled = signal("rolled")
roll_succeeded = signal("roll_succeeded")
roll_failed = signal("roll_failed")

tournament_started = signal("tournament_started")
tournament_ended = signal("tournament_ended")

tournament_round_started = signal("tournament_round_started")
tournament_round_ended = signal("tournament_round_ended")
