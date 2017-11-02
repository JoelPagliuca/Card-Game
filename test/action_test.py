"""
"""
from mock import patch

from base_test import CGTestCase
from card_game.action import *

class PlayCardTest(CGTestCase):
	def test_run(self):
		card = self.card1
		self.gm.current_player().take_card(card)
		act = PlayCard(card)
		act.run(self.gm)

class ReverseTest(CGTestCase):
	@patch('card_game.engine.GameManager.change_direction')
	def test_run(self, change_direction_mock):
		rev = Reverse(self.card1)
		rev.run(self.gm)
		change_direction_mock.assert_called_once()
