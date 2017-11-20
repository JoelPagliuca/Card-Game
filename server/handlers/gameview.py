"""
Handler for viewing/interacting with the game
"""
import logging
import json
import threading
import time

import names

from base import BaseHandler
from server.util import WebSocketInterface
from data import CLIENTS, GAMES

from card_game import constants
from card_game.player import Player
from card_game.engine import GameManager
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECK

__all__ = ["GameViewHandler"]

MAX_PLAYERS = 2
PLAYERS = []

GAME_MANAGER = None # the game manager for everything

def start_game():
	"""
	background a game instance, 
	connect all the clients to the game
	"""
	global GAME_MANAGER
	GAME_MANAGER = GameManager(PLAYERS, GET_DECK(), RULES)
	GAME_MANAGER.interface = WebSocketInterface
	for _, client in CLIENTS.items():
		GAME_MANAGER.observe(client)	# FIXME do real observer pattern, client.observe(observable)
	logging.info("Starting game")
	game_thread = threading.Thread(target=GAME_MANAGER.run)
	game_thread.start()

def stop_game():
	global PLAYERS, GAME_MANAGER
	logging.info("Stopping game")
	# remove all players, close their connections, kill the game
	PLAYERS[:] = []
	for player in CLIENTS:
		GAME_MANAGER.deleteObserver(CLIENTS[player])
		CLIENTS[player].close()	# FIXME write out a GAME_OVER message to the client
	CLIENTS.clear()
	GAME_MANAGER = None

class GameViewHandler(BaseHandler):
	"""communicates with a client and game instance"""
	
	def __init__(self, application, request, **kwargs):
		super(BaseHandler, self).__init__(application, request, **kwargs)
		global GAME_MANAGER, PLAYERS
		self.player = Player(names.get_full_name())
		self.client_id = self.player.secret
		# stop the webserver crashing when there's too many players
		if len(PLAYERS) == MAX_PLAYERS:
			stop_game()
		PLAYERS.append(self.player)
		CLIENTS[self.player] = self
		self.input = None
		logging.info("New handler created for "+self.player.name)

	def open(self):
		"""start a new player's connection"""
		global GAME_MANAGER
		logging.info("Opened connection for client "+self.client_id)
		# start the game
		if not GAME_MANAGER and len(PLAYERS) >= 2:	# FIXME this logic should not be here probably
			logging.info("Got enough player connections, starting a game")
			start_game()
	
	def on_message(self, message):
		"""get an input from the user"""
		message = json.loads(message)
		input_ = message.get('input', "")
		self.input = input_
		logging.info("got "+self.input+" from "+self.player.name)
	
	def on_close(self):
		"""stop the running game"""
		try:
			logging.info(self.client_id+" disconnect. Ending game")
			stop_game()
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
		players = data.get(constants.CONTEXT.PLAYERS)
		output = {
			"action": ACTION.UPDATE,
			"current_player": current_player.toDict(),
			"players": map(lambda p:p.toDict(), players),
			"hand": map(lambda c:c.toDict(), self.player.hand),
			"top_card": top_card.toDict(),
		}
		self.write_message(output)
