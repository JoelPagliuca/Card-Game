"""
"""
from mock import patch

from base_test import CGTestCase
from card_game.action import *
from card_game.action import Action

class ActionTest(CGTestCase):
	def test_id_generation(self):
		rev1 = Action(self.card1,"1",[PlayCard, Reverse])
		self.assertIsNotNone(rev1.id)
		rev2 = Action(self.card2,"2",[PlayCard, Reverse])
		self.assertNotEqual(rev1.id, rev2.id)
	
	def test_to_dict(self):
		card = self.card1
		act = Action(card,"",[])
		d = act.toDict()
		self.assertTrue(d.has_key("description"))
		self.assertTrue(d.has_key("card"))
		self.assertEqual(card.id, d["card"]["id"])

class EffectTest(CGTestCase):
	def test_init(self):
		with self.assertRaises(Exception):
			Effect.apply(None, None)

class PlayCardTest(CGTestCase):
	def test_play_card(self):
		card = self.card1
		player = self.gm.current_player()
		player.take_card(card)
		PlayCard.apply(card, self.gm)
		self.assertEqual(card, self.gm.pile.top_card())

class DrawCardTest(CGTestCase):
	def test_draw_card(self):
		player = self.gm.current_player()
		num_cards = len(player.hand)
		DrawCard.apply(None, self.gm)
		self.assertEqual(len(player.hand)-1, num_cards)

class ReverseTest(CGTestCase):
	@patch('card_game.engine.GameManager.change_direction')
	def test_reverse(self, change_direction_mock):
		self.gm.current_player().take_card(self.card1)
		Reverse.apply(self.card1, self.gm)
		change_direction_mock.assert_called_once()

class SkipTest(CGTestCase):
	def test_skip(self):
		p1 = self.gm.current_player()
		self.gm.current_player().take_card(self.card1)
		# figure out who the next player should be after skip
		self.gm.next_player()
		self.gm.next_player()
		p_next = self.gm.current_player()
		p = self.gm.current_player()
		# go back to that first player
		self.gm.change_direction()
		self.gm.next_player()
		self.gm.next_player()
		self.assertEqual(p1, self.gm.current_player())
		Skip.apply(self.card1, self.gm)
		self.assertEqual(self.gm.current_player(), p_next)
	