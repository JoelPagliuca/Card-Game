"""
Classes related to a game player
"""
__all__ = ["Player"]

class Player(object):
	"""
	A Player
	"""
	def __init__(self, name):
		"""
		:type name: str
		"""
		self.name = name
		self.hand = list()
	
	def take_card(self, card):
		"""
		:type card: Card
		"""
		self.hand.append(card)