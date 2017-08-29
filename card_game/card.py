"""
All classes related to Cards
"""
import random

import constants

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
		:type name: str
		:type cards: list
		"""
		self.name = name
		self._cards = []
		self._cards.extend(cards)
		self._initialize()
	
	def _initialize(self):
		random.shuffle(self._cards)

	def draw_card(self):
		"""
		:rtype: Card
		"""
		return self._cards.pop()

	def restock(self, cards):
		"""
		add more cards to the deck
		:type cards: list
		"""
		self._cards.extend(cards)
		self._initialize()
	
	def need_to_shuffle(self):
		"""
		:rtype: bool
		"""
		return len(self._cards) == 0

class Pile(object):
	"""
	Where you put cards
	last card in the list is the top card
	"""
	def __init__(self):
		self._cards = []
	
	def play_card(self, a_card):
		"""
		Put a card on the top of the deck
		:type a_card: Card
		"""
		self._cards.append(a_card)

	def top_card(self):
		"""
		:rtype: Card
		"""
		return self._cards[-1]

	def take_cards(self):
		"""
		Clear the pile and return the cards
		:rtype: list
		"""
		output = []
		output.extend(self._cards)
		self._cards = []
		return output
