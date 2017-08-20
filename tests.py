"""
All the tests
"""
from unittest import TestCase

from main import *

class CGTestCase(TestCase):

	def setUp(self):
		self.card1 = Card(1, "blue")
		self.card2 = Card(2, "blue")
		self.deck = Deck("test", [self.card1, self.card2])
		self.pile = Pile()

class AllTests(CGTestCase):
	
	def test_draw_card(self):
		a_card1 = self.deck.draw_card()
		a_card2 = self.deck.draw_card()
		self.assertIn(a_card1, [self.card1, self.card2])
		self.assertIn(a_card2, [self.card1, self.card2])

class PileTests(CGTestCase):

	def test_pile(self):
		self.pile.play_card(self.card1)
		self.assertEqual(self.card1, self.pile.top_card())