"""
"""
from base_test import CGTestCase

class CardTests(CGTestCase):
	
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
	
	def test_num_cards(self):
		self.assertEqual(self.deck.num_cards(), len(self.deck._cards))
	
	def test_pile(self):
		self.pile.play_card(self.card1)
		self.assertEqual(self.card1, self.pile.top_card())
	
	def test_take_cards(self):
		self.pile.play_card(self.card1)
		self.pile.play_card(self.card2)
		self.assertItemsEqual(self.cards, self.pile.take_cards())
	
	def test_need_to_shuffle(self):
		# draw all the cards then check if we need to shuffle
		no_cards = len(self.cards)
		for _ in range(no_cards):
			self.assertFalse(self.deck.need_to_shuffle())
			self.deck.draw_card()
		self.assertTrue(self.deck.need_to_shuffle())
	
	def test_to_dict(self):
		d = self.card1.toDict()
		self.assertEqual(d['value'], self.card1.value)
		self.assertEqual(d['suit'], self.card1.suit)
		self.assertEqual(d['id'], self.card1.id)
