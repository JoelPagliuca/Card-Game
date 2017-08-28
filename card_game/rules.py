"""
Rule sets for the game
"""
import constants

__all__ = ["SimpleRules"]

class Rules(object):
	"""
	Implements the game rules
	"""
	@classmethod
	def can_be_played(cls, card, context={}):
		"""
		:rtype: bool
		"""
		pass #TODO
	
	@classmethod
	def check_for_win(cls, context={}):
		"""
		checks to see if the game has been won yet
		:rtype: Player
		"""
		pass # TODO

class SimpleRules(Rules):
	"""
	Basically just put any card on top of another
	"""
	def can_be_played(cls, card, context={}):
		return True

	def check_for_win(cls, context={}):
		players = context.get(constants.CONTEXT_PLAYERS, [])
		for p in players:
			if len(player.hand) == 0:
				return p
		return None