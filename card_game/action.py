"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
All actions will be given pointers to the card and game_manager
Assume that the current player is who played the card with the action
"""
from abc import ABCMeta, abstractmethod

import constants

__all__ = ["Action", "Effect", "PlayCard", "DrawCard", "Reverse", "Skip", "PlusTwo", "ChangeSuitBlue", "ChangeSuitPurple", "ChangeSuitRed", "ChangeSuitYellow"]

class Action(object):
	"""
	Base class for all actions

	:ivar str id: so we can reference
	:ivar Card card: card the action originates from
	:ivar str description: what this action will do
	:ivar list effects: effects to be applied on action run
	"""
	_TAG = "ACTION"
	def __init__(self, card, description="", effects=[]):
		"""
		:param card: keep this reference for later
		:type card: :class:`card_game.card.card`
		:param str description: description of action
		:param list effects: 
		"""
		self.card = card
		self.id = str(id(self))
		self.description = description
		self.effects = effects
	
	def toDict(self):
		"""
		Convert to JSON string

		:rtype: dict(str, str)
		"""
		output = { "action": self.description, "id": self.id, "description": self.description }
		if self.card:
			output["card"] = self.card.toDict()
		return output
	
	def run(self, game_manager):
		"""
		Make the action happen

		:param game_manager:
		:type game_manager: :class:`card_game.engine.GameManager`
		"""
		for effect in self.effects:
			effect.apply(self.card, game_manager)
	
	def has_effect(self, effect):
		"""
		checks for an action with this effect

		:param str effect: the effect we're checking
		:rtype: bool
		"""
		output = False
		for eff in self.effects:
			if eff.has_effect(effect):
				output = True
		return output

class Effect(object):
	"""
	Base class for all Effects, 
	these implement the special cards in the game
	"""
	__metaclass__ = ABCMeta
	@abstractmethod
	def apply(cls, card, game_manager):
		raise NotImplemented()
	
	def has_effect(cls, effect):
		"""
		checks for an action with this effect

		:param str effect: the effect we're checking
		:rtype: bool
		"""
		return False

class PlayCard(Action):
	"""Just play the card"""
	@classmethod
	def apply(cls, card, game_manager):
		player = game_manager.current_player()
		player.hand.remove(card)
		game_manager.pile.play_card(card)

class DrawCard(Action):
	"""Pick up the top card according to how many effects are stacked up.
	Then resets the current effect"""
	@classmethod
	def apply(cls, card, game_manager):
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
	@classmethod
	def apply(cls, card, game_manager):
		game_manager.change_direction()

class Skip(PlayCard):
	"""Reverse direction of gameplay"""
	@classmethod
	def apply(cls, card, game_manager):
		game_manager.next_player()

class PlusTwo(PlayCard):
	def has_effect(cls, effect):
		"""actually checking if there's a PLUS2 in effect"""
		return effect == constants.CONTEXT.EFFECTS.DRAW_TWO
	
	@classmethod
	def apply(cls, card, game_manager):
		ctx = game_manager.get_context()
		ctx[constants.CONTEXT.CURRENT_EFFECT] = constants.CONTEXT.EFFECTS.DRAW_TWO
		current_stack = ctx.get(constants.CONTEXT.CURRENT_EFFECT_VALUE, 0)
		current_stack += 2
		ctx[constants.CONTEXT.CURRENT_EFFECT_VALUE] = current_stack

# these are separate classes to avoid making all effects used as objects
class ChangeSuitBase(Effect):
	NEW_SUIT = ""
	@classmethod
	def apply(cls, card, game_manager):
		card.suit = cls.NEW_SUIT

class ChangeSuitBlue(ChangeSuitBase):
	NEW_SUIT = constants.CARD_BLUE

class ChangeSuitRed(ChangeSuitBase):
	NEW_SUIT = constants.CARD_RED

class ChangeSuitYellow(ChangeSuitBase):
	NEW_SUIT = constants.CARD_YELLOW

class ChangeSuitPurple(ChangeSuitBase):
	NEW_SUIT = constants.CARD_PURPLE