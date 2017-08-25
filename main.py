"""
All the code for the moment
"""
import random

__all__ = ["Card", "Deck", "Pile", "GameManager", "Player", "Hand"]

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
		"""
		self._cards.extend(cards)
		self._initialize()

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

	def take_cards(self):
		output = []
		output.extend(self._cards)
		self._cards = []
		return output

class GameManager(object):
	pass

class Hand(object):
	"""
	A player's hand of cards
	"""
	def __init__(self):
		self._cards = []

class Player(object):
	"""
	A Player
	"""
	def __init__(self, name):
		self.name = name
		self.hand = Hand()