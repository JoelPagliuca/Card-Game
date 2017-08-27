"""
"""
from mock import patch

from base_test import CGTestCase

class EngineTests(CGTestCase):
	pass

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