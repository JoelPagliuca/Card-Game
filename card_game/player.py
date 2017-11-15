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
		self.id = str(id(self))
		self.secret = str(uuid.uuid4())	# maybe could use this to verify whether we can see the hand?
		self.name = name
		self.hand = list()
		self._human = is_human
	
	def take_card(self, card):
		"""
		:type card: Card
		"""
		self.hand.append(card)
	
	def is_human(self): # pragma: no cover
		return self._human

	def toDict(self, censored=True):
		"""
		:param censored: not everyone needs to know the player id
		:rtype: dict
		"""
		data = {"id": self.id, "name": self.name, "num_cards": len(self.hand)}
		if censored:
			return data
		else:
			data["hand"] = map(lambda c:c.toDict(), self.hand)
			return data

	def __hash__(self): # pragma: no cover
		return hash(self.id)