"""
Handler for viewing/interacting with the game
"""
import logging
import json
import threading
import uuid
import time

from base import BaseHandler

from card_game import constants
from card_game.player import Player
from card_game.engine import GameManager, TextInterface
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECKs

__all__ = ["GameViewHandler"]

PLAYERS = []

GAME_MANAGER = None # the game manager for everything

CLIENTS = {}		# Player -> Handler

def start_game():
	"""
	background a game instance
	connect all the clients to the game
	"""
	GAME_MANAGER = GameManager(PLAYERS, GET_DECK(), RULES)
	GAME_MANAGER.interface = WebSocketInterface
	for _, client in CLIENTS.items():
		GAME_MANAGER.observe(client)
	logging.info("Starting game")
	game_thread = threading.Thread(target=GAME_MANAGER.run)
	game_thread.start()

class GameViewHandler(BaseHandler):
	"""
	communicates with the clients and game instance
	"""
	
	def __init__(self, application, request, **kwargs):
		super(BaseHandler, self).__init__(application, request, **kwargs)
		self.player = Player("Player") # TODO https://github.com/treyhunner/names
		self.client_id = self.player.id
		PLAYERS.append(self.player)
		CLIENTS[self.player] = self
		self.input = None
		logging.info("New handler created for "+self.player.name)

	def open(self):
		"""
		start a new player's connection
		"""
		global GAME_MANAGER
		logging.info("Opened connection for client "+self.client_id)
		# start the game
		if not GAME_MANAGER and len(PLAYERS) >= 2:	# FIXME this logic should not be here probably
			logging.info("Got enough player connections, starting a game")
			start_game()
	
	def on_message(self, message):
		"""
		get an input from the user
		"""
		message = json.loads(message)
		input_ = message.get('input', "")
		self.input = input_
		logging.info("got "+self.input+" from "+self.player.name)
	
	def on_close(self):
		"""
		stop the running game
		# FIXME take this client off the update list
		"""
		global GAME_MANAGER
		try:	
			GAME_MANAGER.running = False
			GAME_MANAGER = None
			logging.info(self.client_id+" disconnect. Game ended")
		except:
			pass
	
	def update(self, data):
		"""
		receive the game context from the GameManager
		:type data: dict
		"""
		logging.info("Update from the game")
		current_player = data.get(constants.CONTEXT.CURRENT_PLAYER)
		top_card = data.get(constants.CONTEXT.TOP_CARD)
		# FIXME the json serializing here could be a bit cleaner
		output = {
			"action": ACTION.UPDATE,
			"current_player": {k: current_player.__dict__[k] for k in ('name',)},
			"top_card": {k: top_card.__dict__[k] for k in ('value', 'suit')},
		}
		self.write_message(output)

class WebSocketInterface(TextInterface):
	"""
	Gets user input over WebSocket
	"""
	TAG = "WS_IFACE"
	@classmethod
	def render(cls, msg):
		pass
	
	@classmethod
	def get_input(cls, prompt=None, player=None):
		"""
		gets a string from the user
		wait for string from the WebSocket client
		:type prompt: str
		:rtype: str
		"""
		logging.debug("Taking input from "+player.name, cls.TAG)
		client = CLIENTS[player]
		while True:
			if client.input:
				output = client.input
				client.input = None
				return output
			time.sleep(0.1)
	
	@classmethod
	def get_choice(cls, options, prompt="", player=None):
		"""
		get a choice from a user
		user will see choices in 1 indexed form
		:param options: list of descriptions to present to the user
		:type options: list
		:return: the item chosen from the list (0 index)
		:rtype: int
		"""
		data = {}
		client = CLIENTS[player]
		for i in range(len(options)):
			data[i+1] = str(options[i])
		data.update({"action": ACTION.OPTION})
		client.write_message(data)
		choice = -1
		while not choice in range(len(options)):
			choice = cls.get_int(prompt, player)-1
		return choice

class ACTION():
	"""
	message types being sent to the client
	"""
	UPDATE = "UPDATE"	# game state update
	OPTION = "OPTION"	# request option selection from user