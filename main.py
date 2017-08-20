"""
All the code for the moment
"""
import random

__all__ = ["Card", "Deck", "Pile"]

class Card(object):
	"""
	"""
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

class Deck(object):
	"""
	A set of cards
	"""
	def __init__(self, name="deck", cards=[]):
		"""
		side effect may shuffle the card list
		"""
		self.name = name
		self._cards = cards
		random.shuffle(self._cards)

	def draw_card(self):
		"""
		:rtype: Card
		"""
		return self._cards.pop()

class Pile(object):
	"""
	Where you put cards
	last card in the list is the top card
	"""
	def __init__(self):
		self._cards = []
	
	def play_card(self, a_card):
		"""
		:type a_card: Card
		"""
		self._cards.append(a_card)

	def top_card(self):
		"""
		:rtype: Card
		"""
		return self._cards[-1]
