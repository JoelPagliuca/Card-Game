"""
All the code that makes the game run
"""
import random

from card import Pile
from util import *

__all__ = ["GameManager", "TextInterface"]

class GameManager(object): # pragma: no cover
	"""
	Runs the game
	"""
	TAG = "GAMEMANAGER"

	def __init__(self, players, deck, rules):
		"""
		:type players: list
		:type deck: Deck
		:type rules: Rules
		"""
		self.players = []
		self._current_player = 0
		self._direction = 1
		self.deck = deck
		self.pile = Pile()
		self.rules = rules
	
	def next_player(self):
		"""
		change the current player
		"""
		pass #TODO
	
	def current_player(self):
		"""
		get the current player in the list
		:rtype: Player
		"""
		pass #TODO
	
	def change_direction(self):
		pass #TODO

	def _preRun(self):
		self._current_player = 0
		Logger.debug("starting game", self.TAG)

	def run(self):
		"""
		Play the game
		"""
		_preRun()
		pass

class TextInterface(object):
	"""
	Gets user input over terminal
	"""
	def get_input(self, prompt=None):
		"""
		gets a string from the user
		:type prompt: str
		:rtype: str
		"""
		return input(prompt)

	def get_int(self, prompt=None):
		output = None
		while not output:
			output = None
			try:
				output = int(self.get_input(prompt))
			except ValueError:
				print "That was not an integer"
		return output

	def get_choice(self, options, prompt=""):
		"""
		get a choice from a user
		user will see choices in 1 indexed form
		:param options: list of descriptions to present to the user
		:type options: list
		:return: the item chosen from the list (0 index)
		:rtype: int
		"""
		for i in range(len(options)):
			print "{}: {}".format(str(i+1), options[i])
		choice = -1
		while not choice in range(len(options)):
			choice = self.get_int(prompt)
		return choice-1
