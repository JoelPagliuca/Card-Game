"""
All the code for the moment
"""

__all__ = ["Card", "Deck"]

class Card(object):
	
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

class Deck(object):
	
	def __init__(self, name="deck", cards=[]):
		self.name = name
		self._cards = cards

	def draw_card(self):
		"""
		:rtype: Card
		"""
		pass