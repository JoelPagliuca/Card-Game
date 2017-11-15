"""
"""
from mock import patch, MagicMock, ANY

from base_test import CGTestCase

from card_game import constants
from card_game import action
from card_game.rules import SimpleRules

class EngineTests(CGTestCase):
	
	def test_next_player(self):
		p1 = self.gm.current_player()
		self.assertEqual(p1, self.players[0])
		self.gm.next_player()
		p2 = self.gm.current_player()
		self.assertEqual(p2, self.players[1])
		self.gm.next_player()
		p3 = self.gm.current_player()
		self.assertEqual(p3, self.players[2])
		self.gm.next_player()
		p4 = self.gm.current_player()
		self.assertEqual(p4, p1)
	
	def test_change_direction(self):
		self.gm.change_direction()
		p1 = self.gm.current_player()
		self.assertEqual(p1, self.players[0])
		self.gm.next_player()
		p2 = self.gm.current_player()
		self.assertEqual(p2, self.players[2])
		self.gm.next_player()
		p3 = self.gm.current_player()
		self.assertEqual(p3, self.players[1])
		self.gm.next_player()
		p4 = self.gm.current_player()
		self.assertEqual(p4, p1)
	
	def test_who_shuffled(self):
		self.gm.who_shuffled()
		self.assertGreater(len(self.player1.hand), 0)
		self.assertGreater(len(self.player2.hand), 0)
		self.assertGreater(len(self.player3.hand), 0)
		self.gm.shuffle()
	
	def test_get_options(self):
		opts = self.gm.get_options(self.player1)
		self.assertIsInstance(opts[0], action.DrawCard)
		self.gm.who_shuffled()
		opts = self.gm.get_options(self.player1)
		self.assertEqual(len(opts), self.gm.rules.CARDS_TO_DEAL+1) # now 1 option per card + draw card

	def test_shuffle(self):
		cards_in_deck = len(self.gm.deck._cards)
		self.gm.who_shuffled() # all players have x cards
		for p in self.players:
			for _ in range(self.gm.rules.CARDS_TO_DEAL):
				self.gm.pile.play_card(p.hand.pop())
		self.assertLess(len(self.gm.deck._cards), cards_in_deck) # just make sure some cards are now out of the deck
		self.gm.shuffle()
		self.assertEqual(len(self.gm.deck._cards), cards_in_deck)
	
	def test_update_state(self):
		# see if some stuff was added to the context
		starting_keys = self.gm._context.keys()
		self.gm.who_shuffled()
		self.gm.update_state()
		self.assertGreater(len(self.gm._context.keys()), len(starting_keys))
	
	def test_observe(self):
		# check if an observer is added to the observers list
		dummy = MagicMock() # will have .update function ;)
		self.gm.observe(dummy)
		self.assertListEqual(self.gm._observers, [dummy])
		self.gm.deleteObserver(dummy)
		self.assertListEqual(self.gm._observers, [])
	
	def test_observe_contract(self):
		# make sure we have a tantrum if the observer cannot observe
		dummy = MagicMock()
		dummy.update = None
		with self.assertRaises(Exception):
			self.gm.observe(dummy)
		self.assertListEqual(self.gm._observers, [])
	
	@patch.object(SimpleRules, 'cards_to_deal')
	def test_who_shuffled_too_many_cards(self, mock):
		mock.return_value = 50
		with self.assertRaises(AssertionError):
			self.gm.who_shuffled()
	
	def test_update_observers(self):
		# check if the observers are updated
		dummy = MagicMock()
		self.gm.observe(dummy)
		self.gm.update_observers()
		dummy.update.assert_called_once_with(ANY)

class TextInterfaceTests(CGTestCase):
	
	@patch("__builtin__.raw_input", return_value=2)
	def test_get_int(self, mock):
		value = self.ti.get_int()
		self.assertEqual(value, 2)
	
	@patch("__builtin__.raw_input", side_effect=["password=", "secret_key", "exit()", "2"])
	def test_get_int_sad(self, mock):
		value = self.ti.get_int()
		self.assertEqual(value, 2)

	@patch("__builtin__.raw_input", side_effect=["aws_secret", "-123", "123", "1+1", "4", "3"])
	def test_get_choice_sad(self, mock):
		options = ["zero", "one", "two (option 3)"]
		value = self.ti.get_choice(options)
		self.assertEqual(value, options[2])