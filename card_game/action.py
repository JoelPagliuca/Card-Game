"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
All actions will be given pointers to the card and game_manager
Assume that the current player is who played the card with the action
"""
from abc import ABCMeta, abstractmethod

import constants

__all__ = ["Action", "PlayCard", "DrawCard", "Reverse", "Skip", "PlusTwo", "ChangeSuit"]

class Action(object):
	"""
	Base class for all actions

	:ivar str id: so we can reference
	:ivar Card card: card the action originates from
	:ivar str description: what this action will do
	"""
	__metaclass__ = ABCMeta
	_TAG = "ACTION"
	def __init__(self, card, description=""):
		"""
		:param card: keep this reference for later
		:type card: :class:`card_game.card.card`
		:param str description: description of action
		"""
		self.card = card
		self.id = str(id(self))
		self.description = description
		self.effects = []
	
	def toDict(self):
		"""
		Convert to JSON string

		:rtype: dict(str, str)
		"""
		output = { "action": self._TAG, "id": self.id }
		if self.card:
			output["card"] = self.card.toDict()
		return output
	
	@abstractmethod
	def run(self, game_manager):
		"""
		Make the action happen

		:param game_manager:
		:type game_manager: :class:`card_game.engine.GameManager`
		"""
		raise NotImplementedError()
	
	def has_effect(self, effect):
		"""
		checks for an action with this effect

		:param str effect: the effect we're checking
		:rtype: bool
		"""
		return False

class Effect(object):
	#TODO convert all actions to effects
	@classmethod
	def apply(cls, card, game_manager):
		raise NotImplemented()

class PlayCard(Action):
	"""Just play the card"""
	_TAG = "PLAY"
	def run(self, game_manager):
		player = game_manager.current_player()
		player.hand.remove(self.card)
		game_manager.pile.play_card(self.card)

class DrawCard(Action):
	"""Pick up the top card according to how many effects are stacked up.
	Then resets the current effect"""
	_TAG = "DRAW"
	def run(self, game_manager):
		amount = 1
		ctx = game_manager.get_context()
		if ctx.get(constants.CONTEXT.CURRENT_EFFECT_VALUE, 0):
			amount = ctx[constants.CONTEXT.CURRENT_EFFECT_VALUE]
		for _ in range(amount):
			top_card = game_manager.deck.draw_card()
			game_manager.current_player().take_card(top_card)
		ctx[constants.CONTEXT.CURRENT_EFFECT] = None
		ctx[constants.CONTEXT.CURRENT_EFFECT_VALUE] = 0
		

class Reverse(PlayCard):
	"""Reverse direction of gameplay"""
	_TAG = "REVERSE"
	def run(self, game_manager):
		super(Reverse, self).run(game_manager)
		game_manager.change_direction()

class Skip(PlayCard):
	"""Reverse direction of gameplay"""
	_TAG = "SKIP"
	def run(self, game_manager):
		super(Skip, self).run(game_manager)
		game_manager.next_player()

class PlusTwo(PlayCard):
	_TAG = "PLUS2"

	def has_effect(self, effect):
		"""actually checking if there's a PLUS2 in effect"""
		return effect == constants.CONTEXT.EFFECTS.DRAW_TWO

	def run(self, game_manager):
		super(PlusTwo, self).run(game_manager)
		ctx = game_manager.get_context()
		ctx[constants.CONTEXT.CURRENT_EFFECT] = constants.CONTEXT.EFFECTS.DRAW_TWO
		current_stack = ctx.get(constants.CONTEXT.CURRENT_EFFECT_VALUE, 0)
		current_stack += 2
		ctx[constants.CONTEXT.CURRENT_EFFECT_VALUE] = current_stack

class ChangeSuit(PlayCard):
	_TAG = "WILD"

	def __init__(self, card, suit=constants.CARD_RED):
		super(ChangeSuit, self).__init__(card)
		self.new_suit = suit
	
	def toDict(self):
		output = super(ChangeSuit, self).toDict()
		output['new_suit'] = self.new_suit
		return output

	def run(self, game_manager):
		super(ChangeSuit, self).run(game_manager)
		self.card.suit = self.new_suit
