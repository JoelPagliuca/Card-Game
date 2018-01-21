"""
"""
from mock import patch

from base_test import CGTestCase
from card_game.action import *
from card_game.action import Action

# class ActionTest(CGTestCase):
# 	def test_init(self):
# 		with self.assertRaises(Exception):
# 			act = Action(self.card1)

class EffectTest(CGTestCase):
	def test_init(self):
		with self.assertRaises(Exception):
			eff = Effect()

class PlayCardTest(CGTestCase):
	def test_play_card(self):
		card = self.card1
		player = self.gm.current_player()
		player.take_card(card)
		act = PlayCard(card)
		act.run(self.gm)
		self.assertEqual(card, self.gm.pile.top_card())
	
	def test_to_dict(self):
		card = self.card1
		act = PlayCard(card)
		d = act.toDict()
		self.assertTrue(d.has_key("action"))
		self.assertTrue(d.has_key("card"))
		self.assertEqual(card.id, d["card"]["id"])

class DrawCardTest(CGTestCase):
	def test_draw_card(self):
		player = self.gm.current_player()
		num_cards = len(player.hand)
		act = DrawCard(None)
		act.run(self.gm)
		self.assertEqual(len(player.hand)-1, num_cards)
	
	def test_to_dict(self):
		act = DrawCard(None)
		d = act.toDict()
		self.assertFalse(d.has_key("card"))

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

class SkipTest(CGTestCase):
	def test_skip(self):
		p1 = self.gm.current_player()
		self.gm.current_player().take_card(self.card1)
		skip = Skip(self.card1)
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
		skip.run(self.gm)
		self.assertEqual(self.gm.current_player(), p_next)
	