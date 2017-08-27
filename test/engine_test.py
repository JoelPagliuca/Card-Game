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
	
	@patch("__builtin__.input", side_effect=["not int", "also not int", 2])
	def test_get_int_sad(self, mock):
		value = self.ti.get_int()
		self.assertEqual(value, 2)