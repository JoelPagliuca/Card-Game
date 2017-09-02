"""
"""
from mock import patch

from base_test import CGTestCase
from card_game.action import *

class ReverseTest(CGTestCase):
	@patch('card_game.engine.GameManager.change_direction')
	def test_run(self, change_direction_mock):
		Reverse.run(self.gm)
		change_direction_mock.assert_called_once()