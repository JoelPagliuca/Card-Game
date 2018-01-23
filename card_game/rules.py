"""
Rule sets for the game
"""
from abc import ABCMeta, abstractmethod
import logging

import constants
from util import abstractclassmethod
from action import Action, DrawCard

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
	def get_options(cls, player, context={}):
		"""
		figure out what options to present to the user

		:param player: player to get options for
		:type player: :class:`card_game.player.Player`
		:rtype: list(:class:`card_game.action.Action`)
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
	Basically just put any card on top of another, mainly used for unit testing
	"""
	CARDS_TO_DEAL = 7
	@classmethod
	def can_be_played(cls, card, context={}):
		"""
		under the current game context, can card be played

		:param card:
		:type card: :class:`card_game.card.Card`
		:param dict(str,object) context: game context
		:rtype: bool
		"""
		return True

	@classmethod
	def get_options(cls, player, context={}):
		"""
		figure out what options to present to the user

		:param player: player to get options for
		:type player: :class:`card_game.player.Player`
		:rtype: list(:class:`card_game.action.Action`)
		"""
		options = []
		for card in player.hand:
			if cls.can_be_played(card, context):
				options.extend(card.actions)
		options.append(Action(None, "DRAW", [DrawCard]))
		return options
	
	@classmethod
	def check_for_win(cls, context={}):
		"""
		have the win conditions been met?

		:param dict(str,object) context: game context
		:rtype: bool
		"""
		players = context.get(constants.CONTEXT.PLAYERS, [])
		for p in players:
			if len(p.hand) == 0:
				return p
		return None

	@classmethod
	def cards_to_deal(cls, context={}):
		"""
		figure out how many cards to deal out, 
		usually a static number, but for games like cheat it depends on number of players
		
		:param dict(str,object) context: game context
		:rtype: int
		"""
		return cls.CARDS_TO_DEAL

class MelbourneRules(SimpleRules):
	"""
	More complex rules used at the office
	"""
	TAG = "MELBRULES"
	@classmethod
	def can_be_played(cls, card, context={}):
		"""More complex implementation"""
		top_card = context.get(constants.CONTEXT.TOP_CARD, None)
		logging.debug("Trying to play (" + str(card) + ") on (" + str(top_card) + ")")
		# variables used to determine if the card is playable
		suit_match = False
		value_match = False
		effect_match = False
		if top_card:
			# check if the value or suit match
			if (top_card.suit == card.suit) or card.suit == constants.CARD_BLACK:
				suit_match = True
			elif top_card.value == card.value:
				value_match = True
			if context.get(constants.CONTEXT.CURRENT_EFFECT, None):
				effect = context[constants.CONTEXT.CURRENT_EFFECT]
				for act in card.actions:
					if act.has_effect(effect):
						effect_match = True
			else:
				effect_match = True
		else:
			return True
		logging.debug("About to return effect:{}, suit:{}, value:{}".format(effect_match, suit_match, value_match))
		return effect_match and (suit_match or value_match)
