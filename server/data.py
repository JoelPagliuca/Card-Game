"""Stop circular imports with this python file that'll hold all the game data"""

#: so that the WSInterface can find the right client to talk to
CLIENTS = {}	# Player -> Handler
GAMES = {}		# uuid -> GameController

class ACTION():
	"""
	message types being sent to the client
	"""
	UPDATE = "UPDATE"	# game state update
	OPTION = "OPTION"	# request option selection from user
	FINISH = "FINISH"	# game over