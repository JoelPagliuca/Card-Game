"""
Rule sets for the game
"""
import constants

__all__ = ["SimpleRules"]

class Rules(object):
	"""
	Implements the game rules
	ABSTRACT
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

class SimpleRules(Rules):
	"""
	Basically just put any card on top of another
	"""
	@classmethod
	def can_be_played(cls, card, context={}):
		return True
	
	@classmethod
	def check_for_win(cls, context={}):
		players = context.get(constants.CONTEXT_PLAYERS, [])
		print players
		for p in players:
			if len(p.hand) == 0:
				return p
		return None