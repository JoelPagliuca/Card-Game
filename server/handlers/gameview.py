"""
Handler for viewing the game
"""
import logging
import json

from base import BaseHandler

from card_game import constants
from card_game.player import Player
from card_game.engine import GameManager
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECK

__all__ = ["GameViewHandler"]

player1 = Player("Jason")
player2 = Player("Kelly")
player3 = Player("Garth")
players = [player1, player2, player3]

class GameViewHandler(BaseHandler):
	GAME_MANAGER = None
	def open(self):
		logging.info("Got a connection, starting a game")
		# create a new game if one doesn't exist
		if not self.GAME_MANAGER:
			self.GAME_MANAGER = GameManager(players, GET_DECK(), RULES)
		self.GAME_MANAGER.observe(self)
		# run the game if it isn't running
		if not self.GAME_MANAGER.running:
			self.GAME_MANAGER.run()
	
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