"""
All the tests
"""
from unittest import TestCase

from main import *

class AllTests(TestCase):

	def setUp(self):
		self.card1 = Card(1, "blue")
		self.card2 = Card(2, "blue")
		self.card_list = [self.card1, self.card2]
		self.deck = Deck("test", self.card_list)
	
	def test_draw_card(self):
		a_card1 = self.deck.draw_card()
		a_card2 = self.deck.draw_card()
		self.assertIn(a_card1, self.card_list)
		self.assertIn(a_card2, self.card_list)