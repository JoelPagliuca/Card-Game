"""
Classes related to a game player
"""
import uuid

__all__ = ["Player"]

class Player(object):
	"""
	A Player in the game

	:ivar str id: a way to identify the object
	:ivar str secret: used by the websocket server to ID the game client used by the player
	:ivar str name: a name
	:ivar list(Card) hand: cards the player is holding
	"""
	def __init__(self, name, is_human=True):
		"""
		:param str name:
		:param bool is_human:
		"""
		self.id = str(id(self))
		self.secret = str(uuid.uuid4())	# maybe could use this to verify whether we can see the hand?
		self.name = name
		self.hand = list()
		self._human = is_human
	
	def take_card(self, card):
		"""
		:param card:
		:type card: :class:`card_game.card.Card`
		"""
		self.hand.append(card)
	
	def is_human(self): # pragma: no cover
		"""
		:rtype: bool
		"""
		return self._human

	def toDict(self, censored=True):
		"""
		:param bool censored: not everyone needs to know the player's cards
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