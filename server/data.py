"""Stop circular imports with this python file that'll hold all the game data"""

#: so that the WSInterface can find the right client to talk to
CLIENTS = {}		# Player -> Handler
GAMES = {}			# uuid -> GameController