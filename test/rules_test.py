"""
"""
from base_test import CGTestCase

from card_game.rules import *
import card_game.constants as constants

class SimpleRulesTests(CGTestCase):
	def test_can_be_played(self):
		self.assertTrue(SimpleRules.can_be_played(None))
	
	def test_check_for_win(self):
		self.player1.take_card(self.gm.deck.draw_card())
		self.player1.take_card(self.gm.deck.draw_card())
		self.player2.take_card(self.gm.deck.draw_card())
		winner = SimpleRules.check_for_win({constants.CONTEXT_PLAYERS: self.players})
		self.assertEqual(winner, self.player3)
	
	def test_check_for_no_win(self):
		self.player1.take_card(self.gm.deck.draw_card())
		self.player2.take_card(self.gm.deck.draw_card())
		self.player3.take_card(self.gm.deck.draw_card())
		winner = SimpleRules.check_for_win({constants.CONTEXT_PLAYERS: self.players})
		self.assertIsNone(winner)
	
	def test_cards_to_deal(self):
		# super lame test, possible over-engineering
		self.assertEqual(SimpleRules.cards_to_deal(), SimpleRules.CARDS_TO_DEAL)