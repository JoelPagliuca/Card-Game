"""
All the code that makes the game run
"""
import random

import util

__all__ = ["GameManager"]

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

