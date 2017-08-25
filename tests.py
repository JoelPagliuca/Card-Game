"""
All the tests
"""
from unittest import TestCase

from main import *

class CGTestCase(TestCase):

	def setUp(self):
		self.card1 = Card(1, "blue")
		self.card2 = Card(2, "blue")
		self.cards = [self.card1, self.card2]
		self.deck = Deck("test", self.cards)
		self.pile = Pile()
		self.player = Player()

class AllTests(CGTestCase):
	
	def test_draw_card(self):
		a_card1 = self.deck.draw_card()
		a_card2 = self.deck.draw_card()
		self.assertIn(a_card1, self.cards)
		self.assertIn(a_card2, self.cards)
	
	def test_restock_flow(self):
		self.pile.play_card(self.deck.draw_card())
		self.pile.play_card(self.deck.draw_card())
		self.deck.restock(self.pile.take_cards())
		self.assertItemsEqual(self.deck._cards, self.cards)

class PileTests(CGTestCase):

	def test_pile(self):
		self.pile.play_card(self.card1)
		self.assertEqual(self.card1, self.pile.top_card())
	
	def test_take_cards(self):
		self.pile.play_card(self.card1)
		self.pile.play_card(self.card2)
		self.assertItemsEqual(self.cards, self.pile.take_cards())
	