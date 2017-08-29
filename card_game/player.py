"""
Classes related to a game player
"""
__all__ = ["Player"]

class Player(object):
	"""
	A Player
	"""
	def __init__(self, name, is_human=True):
		"""
		:type name: str
		"""
		self.name = name
		self.hand = list()
		self._human = is_human
	
	def take_card(self, card):
		"""
		:type card: Card
		"""
		self.hand.append(card)
	
	def is_human(self):
		return self._human
