"""
All classes related to Cards
"""
import random
import constants

__all__ = ["Card", "Deck", "Pile"]

class Card(object):
	"""
	A generic card

	:ivar str id: so we can reference this card
	:ivar str value: card value
	:ivar str suit: suit or color
	:ivar list(Action) actions: actions this card can be used for, 
		needs to be an array because WILD will have 4 actions
	:ivar str _initial_color: color to revert back to after reshuffle
	"""
	def __init__(self, value, suit):
		"""
		:param str value: card value
		:param str suit: suit or color
		"""
		self.value = value
		self.suit = suit
		self.actions = []
		self.id = str(id(self))
		self._initial_color = suit
	
	def __repr__(self):
		return "Card {} - {}".format(self.value, self.suit)

	def toDict(self):
		"""
		:rtype: dict(str, str)
		"""
		return {"value": self.value, "suit": self.suit, "id": self.id}

	def reset(self):
		"""
		only for wild cards atm, will reset state back to initial state
		"""
		self.suit = self._initial_color

class Deck(object):
	"""A collection of cards"""
	def __init__(self, name="deck", cards=[]):
		"""
		side effect may shuffle the card list

		:param str name:
		:param list(Card) cards:
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

		:param list cards:
		"""
		self._cards.extend(cards)
		self._initialize()
	
	def need_to_shuffle(self):
		"""
		:rtype: bool
		"""
		return len(self._cards) == 0

	def num_cards(self):
		"""
		:rtype: int
		"""
		return len(self._cards)

class Pile(object):
	"""	Where you put cards, last card in the list is the top card"""
	def __init__(self):
		self._cards = []
		self._top_card = None
	
	def play_card(self, a_card):
		"""
		Put a card on the top of the deck

		:param Card a_card:
		"""
		self._cards.append(a_card)
		self._top_card = a_card

	def top_card(self):
		"""
		:rtype: Card
		"""
		if self._top_card:
			return self._top_card
		else:
			return None

	def take_cards(self):
		"""
		Clear the pile and return the cards
		
		:rtype: list(Card)
		"""
		output = []
		output.extend(self._cards)
		for card in output:
			card.reset()
		self._cards = []
		return output
