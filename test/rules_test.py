"""
"""
from base_test import CGTestCase

from card_game.rules import *
from card_game.card import Card
import card_game.constants as constants

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

class MelbourneRulesTests(CGTestCase):
	def test_can_be_played_simple(self):
		ctx = {constants.CONTEXT.TOP_CARD: Card(constants.CARD_ONE, constants.CARD_BLUE)}
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_ONE, constants.CARD_RED), ctx))
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_BLUE), ctx))
		self.assertFalse(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_RED), ctx))
	
	def test_can_be_played_first_card(self):
		ctx = {constants.CONTEXT.TOP_CARD: None}
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_ONE, constants.CARD_RED), ctx))
		self.assertTrue(MelbourneRules.can_be_played(Card(constants.CARD_EIGHT, constants.CARD_BLUE), ctx))