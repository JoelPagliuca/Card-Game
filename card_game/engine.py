"""
All the code that makes the game run
"""
import random

import util

__all__ = ["GameManager", "TextInterface"]

class GameManager(object):
	"""
	Runs the game
	"""
	def __init__(self, players, deck):
		self.players = []
		self._current_player = 0
		self.deck = deck
		self.pile = Pile()

	def _preRun(self):
		self._current_player = 0

	def run(self):
		"""
		Play the game
		"""
		_preRun()

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
		while True:
			output = None
			try:
				output = int(self.get_input(prompt))
			except ValueError:
				print "That was not an integer"
			else:
				break
		return output

class Rules(object):
	"""
	Implements the game rules
	"""
	def can_be_played():
		"""
		"""
		pass