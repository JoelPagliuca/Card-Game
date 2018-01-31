"""
"""
from mock import patch

from base_test import CGTestCase

from card_game.rules import *
from card_game.card import Card
import card_game.constants as constants
from card_game import action

class SimpleRulesTests(CGTestCase):
	def test_can_be_played(self):
		self.assertTrue(SimpleRules.can_be_played(None))
	
	def test_check_for_win(self):
		self.player1.take_card(self.gm.deck.draw_card())
		self.player1.take_card(self.gm.deck.draw_card())
		self.player2.take_card(self.gm.deck.draw_card())
		winner = SimpleRules.check_for_win({constants.CONTEXT.PLAYERS: self.players})
		self.assertEqual(winner, self.player3)
	
	def test_check_for_no_win(self):
		self.player1.take_card(self.gm.deck.draw_card())
		self.player2.take_card(self.gm.deck.draw_card())
		self.player3.take_card(self.gm.deck.draw_card())
		winner = SimpleRules.check_for_win({constants.CONTEXT.PLAYERS: self.players})
		self.assertIsNone(winner)
	
	def test_cards_to_deal(self):
		# super lame test, possible over-engineering
		self.assertEqual(SimpleRules.cards_to_deal(), SimpleRules.CARDS_TO_DEAL)
	
	def test_get_options(self):
		opts = SimpleRules.get_options(self.player1)
		self.assertIsInstance(opts[0], action.Action)
		self.gm.who_shuffled()
		opts = SimpleRules.get_options(self.player1)
		self.assertEqual(len(opts), self.gm.rules.CARDS_TO_DEAL+1) # now 1 option per card + draw card

class MelbourneRulesTests(CGTestCase):
	def test_can_be_played_simple(self):
		ctx = {constants.CONTEXT.TOP_CARD: Card(constants.CARD_ONE, constants.CARD_BLUE)}
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_ONE, constants.CARD_RED), ctx))
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_BLUE), ctx))
		self.assertFalse(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_RED), ctx))
	
	def test_can_be_played_effects(self):
		# test a draw two
		draw_two = Card(constants.CARD_DRAW_TWO, constants.CARD_BLUE)
		another_draw_two = Card(constants.CARD_DRAW_TWO, constants.CARD_PURPLE)
		draw_two.actions.append(action.Action(draw_two,"",[action.PlusTwo]))
		another_draw_two.actions.append(action.Action(another_draw_two,"",[action.PlusTwo]))
		ctx = {constants.CONTEXT.TOP_CARD: draw_two, constants.CONTEXT.CURRENT_EFFECT: constants.CONTEXT.EFFECTS.DRAW_TWO, constants.CONTEXT.CURRENT_EFFECT_VALUE: 2}
		self.assertFalse(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_RED), ctx))
		self.assertFalse(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_BLUE), ctx))
		self.assertTrue(MelbourneRules.can_be_played(another_draw_two, ctx))
	
	def test_can_be_played_first_card(self):
		ctx = {constants.CONTEXT.TOP_CARD: None}
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_ONE, constants.CARD_RED), ctx))
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_BLUE), ctx))
	
	@patch("card_game.rules.MelbourneRules.can_be_played", return_value=False)
	def test_get_options(self, mock):
		ctx = {constants.CONTEXT.TOP_CARD: Card(constants.CARD_ONE, constants.CARD_BLUE)}
		self.gm.who_shuffled()
		opts = MelbourneRules.get_options(self.player1, ctx)
		self.assertIs(opts[0].effects[0], action.DrawCard)