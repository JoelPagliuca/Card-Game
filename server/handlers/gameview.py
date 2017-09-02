"""
Handler for viewing the game
"""
import logging

from base import BaseHandler

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
	def open(self):
		logging.info("Got a connection, starting a game")
		# start a new game if one hasn't already started
		gm = GameManager(players, GET_DECK(), RULES)
		gm.run()
	def on_close(self):
		pass