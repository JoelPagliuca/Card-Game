"""
Classes related to a game player
"""
import uuid

__all__ = ["Player"]

class Player(object):
	"""
	A Player
	"""
	def __init__(self, name, is_human=True):
		"""
		:type name: str
		"""
		self.id = str(uuid.uuid4())
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

	def __hash__(self):
		return hash(self.id)