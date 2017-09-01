"""
Rule sets for the game
"""
import constants

__all__ = ["SimpleRules"]

class Rules(object):
	"""
	Implements the game rules
	ABSTRACT TODO: use abc package
	"""
	@classmethod
	def can_be_played(cls, card, context={}):
		"""
		:rtype: bool
		"""
		raise NotImplementedError()
	
	@classmethod
	def check_for_win(cls, context={}):
		"""
		checks to see if the game has been won yet
		:rtype: Player
		"""
		raise NotImplementedError()
	
	@classmethod
	def cards_to_deal(cls, context={}):
		"""
		figure out how many cards to deal out
		usually a static number, but for games like cheat
			it depends on number of players
		:rtype: int
		"""
		raise NotImplementedError()


class SimpleRules(Rules):
	"""
	Basically just put any card on top of another
	Also used for unit testing
	"""
	CARDS_TO_DEAL = 7
	@classmethod
	def can_be_played(cls, card, context={}):
		return True
	
	@classmethod
	def check_for_win(cls, context={}):
		players = context.get(constants.CONTEXT_PLAYERS, [])
		for p in players:
			if len(p.hand) == 0:
				return p
		return None

	@classmethod
	def cards_to_deal(cls, context={}):
		return cls.CARDS_TO_DEAL