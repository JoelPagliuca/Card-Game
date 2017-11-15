"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
All actions will be given pointers to the card and game_manager
Assume that the current player is who played the card with the action
"""
from abc import ABCMeta, abstractmethod

__all__ = ["Action", "PlayCard", "DrawCard", "Reverse"]

class Action(object):
	"""Base class for all actions
	has a `run` and `toDict` methods
	"""
	__metaclass__ = ABCMeta
	_TAG = "ACTION"
	def __init__(self, card):
		"""
		:param card: keep this reference for later
		:type card: :class:`card_game.card.card`
		"""
		self.card = card
		self.id = str(id(self))
	
	def toDict(self):
		"""
		Convert to JSON string

		:rtype: dict
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

class PlayCard(Action):
	"""Just play the card"""
	_TAG = "PLAY"
	def run(self, game_manager):
		player = game_manager.current_player()
		player.hand.remove(self.card)
		game_manager.pile.play_card(self.card)

class DrawCard(Action):
	"""Pick up the card"""
	_TAG = "DRAW"
	def run(self, game_manager):
		top_card = game_manager.deck.draw_card()
		game_manager.current_player().take_card(top_card)

class Reverse(PlayCard):
	"""Reverse direction of gameplay"""
	_TAG = "REVERSE"
	def run(self, game_manager):
		super(Reverse, self).run(game_manager)
		game_manager.change_direction()
