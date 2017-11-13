"""
"""
from base_test import CGTestCase

class PlayerTests(CGTestCase):
	def test_player_to_dict_censored(self):
		d = self.player1.toDict()
		self.assertFalse(d.has_key("secret"))
		self.assertFalse(d.has_key("hand"))
		self.assertTrue(d.has_key("name"))
		self.assertTrue(d.has_key("id"))
		self.assertTrue(d.has_key("num_cards"))

	def test_player_to_dict_uncensored(self):
		d = self.player1.toDict(False)
		self.assertFalse(d.has_key("secret"))
		self.assertTrue(d.has_key("hand"))
		self.assertTrue(d.has_key("name"))
		self.assertTrue(d.has_key("id"))
		self.assertTrue(d.has_key("num_cards"))
		self.player1.hand = []