"""
Rule sets for the game
"""
from abc import ABCMeta, abstractmethod

import constants
from util import Logger, abstractclassmethod

__all__ = ["SimpleRules", "MelbourneRules"]

class Rules(object):
	"""
	Implements the game rules
	"""
	__metaclass__ = ABCMeta

	@abstractclassmethod
	def can_be_played(cls, card, context={}):
		"""
		:rtype: bool
		"""
		raise NotImplementedError()
	
	@abstractclassmethod
	def check_for_win(cls, context={}):
		"""
		checks to see if the game has been won yet
		:rtype: Player
		"""
		raise NotImplementedError()
	
	@abstractclassmethod
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
		players = context.get(constants.CONTEXT.PLAYERS, [])
		for p in players:
			if len(p.hand) == 0:
				return p
		return None

	@classmethod
	def cards_to_deal(cls, context={}):
		return cls.CARDS_TO_DEAL

class MelbourneRules(SimpleRules):
	"""
	More complex rules used at the office
	"""
	TAG = "MELBRULES"
	@classmethod
	def can_be_played(cls, card, context={}):
		top_card = context.get(constants.CONTEXT.TOP_CARD, None)
		Logger.debug("Trying to play (" + str(card) + ") on (" + str(top_card) + ")")
		if top_card:
			# check if the value or suit match
			if top_card.suit == card.suit:
				return True
			elif top_card.value == card.value:
				return True
		else:
			return True
		return False