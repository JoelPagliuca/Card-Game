"""
"""
from mock import patch

from base_test import CGTestCase

class EngineTests(CGTestCase):
	
	def test_next_player(self):
		p1 = self.gm.current_player()
		self.gm.next_player()
		p2 = self.gm.current_player()
		self.assertEqual(p1, self.players[0])
		self.assertEqual(p2, self.players[1])
	
	def test_change_direction(self):
		p1 = self.gm.current_player()
		self.gm.change_direction()
		self.gm.next_player()
		p2 = self.gm.current_player()
		self.assertEqual(p1, self.players[0])
		self.assertEqual(p2, self.players[-1])

class TextInterfaceTests(CGTestCase):
	
	@patch("__builtin__.input", return_value=2)
	def test_get_int(self, mock):
		value = self.ti.get_int()
		self.assertEqual(value, 2)
	
	@patch("__builtin__.input", side_effect=["password=", "secret_key", "2"])
	def test_get_int_sad(self, mock):
		value = self.ti.get_int()
		self.assertEqual(value, 2)

	@patch("__builtin__.input", side_effect=["aws_secret", "-123", "123", "3", "2"])
	def test_get_choice_sad(self, mock):
		options = ["zero", "one", "two"]
		value = self.ti.get_choice(options)
		self.assertEqual(value, 1)