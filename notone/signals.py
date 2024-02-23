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

stress_test_started = signal("stress_test_started")
stress_test_ended = signal("stress_test_ended")

stress_test_game_started = signal("stress_test_game_started")
stress_test_game_ended = signal("stress_test_game_ended")

stress_test_player_started = signal("stress_test_player_started")
stress_test_player_ended = signal("stress_test_player_ended")
