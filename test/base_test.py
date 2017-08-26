"""
Base for all unit tests
"""
from unittest import TestCase

from card_game.card import *
from card_game.player import *
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
		self.player = Player("test")