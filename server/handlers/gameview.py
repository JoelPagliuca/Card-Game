"""
Handler for viewing/interacting with the game
"""
import logging
import json
import threading
import time

import names

from base import BaseHandler
from server.util import WebSocketInterface, ACTION
from server import data

from card_game import constants
from card_game.player import Player

__all__ = ["GameViewHandler"]

MAX_PLAYERS = 2
PLAYERS = []

GAME_MANAGER = None # the game manager for everything

class GameViewHandler(BaseHandler):
	"""communicates with a client and game instance"""
	
	def __init__(self, application, request, **kwargs):
		super(BaseHandler, self).__init__(application, request, **kwargs)
		self.player = Player(names.get_full_name())
		self.client_id = self.player.secret
		self.input = None
		self.game_id = None
		logging.info("New handler created for "+self.player.name)

	def open(self, game_id):
		"""start a new player's connection, add it to the game controller"""
		logging.info("Opened connection for client "+self.client_id)
		self.game_id = game_id
		controller = data.GAMES.get(game_id)
		if not controller:
			self.close()
			return
		controller.add_player(self.player, self)
		data.CLIENTS[self.player] = self
		logging.info("handled game id: "+game_id)
	
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
			data.GAMES[self.game_id].stop_game()
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
