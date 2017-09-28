"""
Handler for viewing the game
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
from card_game.data.decks import GET_UNO_DECK as GET_DECK

__all__ = ["GameViewHandler"]

player1 = Player("Jason")
player2 = Player("Kelly")
player3 = Player("Garth")
PLAYERS = []

GAME_MANAGER = None # the game manager for everything

CLIENTS = {}		# Player -> Handler

class GameViewHandler(BaseHandler):
	
	def __init__(self, application, request, **kwargs):
		super(BaseHandler, self).__init__(application, request, **kwargs)
		self.client_id = str(uuid.uuid4())
		self.player = Player(self.client_id) #FIXME
		PLAYERS.append(self.player)
		CLIENTS[self.player] = self
		self.input = None

	def open(self):
		"""
		start a new player's connection
		"""
		global GAME_MANAGER
		# create a new game if one doesn't exist
		if not GAME_MANAGER:
			logging.info("Got first connection, starting a game")
			GAME_MANAGER = GameManager(PLAYERS, GET_DECK(), RULES)
			GAME_MANAGER.interface = WebSocketInterface
		GAME_MANAGER.observe(self)
		# run the game if it isn't running
		if not GAME_MANAGER.running and len(PLAYERS) >= 1:
			logging.info("Starting game")
			game_thread = threading.Thread(target=GAME_MANAGER.run)
			game_thread.start()
	
	def on_message(self, message):
		"""
		get an input from the user
		"""
		message = json.loads(message)
		input_ = message.get('input', "")
		self.input = input_
	
	def on_close(self):
		"""
		stop the running game
		"""
		global GAME_MANAGER
		GAME_MANAGER.running = False
		GAME_MANAGER = None
	
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
		client.write_message(data)
		choice = -1
		while not choice in range(len(options)):
			choice = cls.get_int(prompt, player)-1
		return choice
