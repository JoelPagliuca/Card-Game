"""
Base for all unit tests
"""
from unittest import TestCase

from card_game.card import *
from card_game.player import *
from card_game.engine import *
from card_game.rules import *
from card_game.data.decks import *
from card_game import constants

__all__ = ["CGTestCase"]

class CGTestCase(TestCase):

	def setUp(self):
		constants.DEBUG = False
		self.card1 = Card(1, "blue")
		self.card2 = Card(2, "blue")
		self.cards = [self.card1, self.card2]
		self.deck = Deck("test", self.cards)
		self.pile = Pile()

		self.player1 = Player("Jason")
		self.player2 = Player("Kelly")
		self.player3 = Player("Garth")
		self.players = [self.player1, self.player2, self.player3]

		self.ti = TextInterface()
		self.gm = GameManager(self.players, GET_SIMPLE_DECK(), SimpleRules)
	
	def tearDown(self):
		pass