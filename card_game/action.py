"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
"""
__all__ = ["PlayCard", "DrawCard", "Reverse"]

class Action(object):
	def __init__(self, card):
		self.card = card
	"""
	Base class
	TODO: abs
	"""
	def run(self, game_manager):
		"""
		Make the action happen
		:type game_manager: GameManager
		"""
		raise NotImplementedError()

class PlayCard(Action):
	"""
	Just play the card
	"""
	def run(self, game_manager):
		pass

class DrawCard(Action):
	def run(self, game_manager):
		"""
		Make the action happen
		:type game_manager: GameManager
		"""
		game_manager.current_player.take_card()

class Reverse(PlayCard):
	def run(self, game_manager):
		super(Reverse, self).run(game_manager)
		game_manager.change_direction()
