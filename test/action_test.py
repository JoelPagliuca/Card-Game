"""
"""
from mock import patch

from base_test import CGTestCase
from card_game.action import *

class PlayCardTest(CGTestCase):
	def test_play_card(self):
		card = self.card1
		player = self.gm.current_player()
		player.take_card(card)
		act = PlayCard(card)
		act.run(self.gm)
		self.assertEqual(card, self.gm.pile.top_card())

class DrawCardTest(CGTestCase):
	def test_draw_card(self):
		player = self.gm.current_player()
		num_cards = len(player.hand)
		act = DrawCard(None)
		act.run(self.gm)
		self.assertEqual(len(player.hand)-1, num_cards)

class ReverseTest(CGTestCase):
	@patch('card_game.engine.GameManager.change_direction')
	def test_reverse(self, change_direction_mock):
		self.gm.current_player().take_card(self.card1)
		rev = Reverse(self.card1)
		rev.run(self.gm)
		change_direction_mock.assert_called_once()
	
	def test_id_generation(self):
		rev1 = Reverse(self.card1)
		self.assertIsNotNone(rev1.id)
		rev2 = Reverse(self.card1)
		self.assertNotEqual(rev1.id, rev2.id)
