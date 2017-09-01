"""
An effect on a card
"""
__all__ = ["Reverse"]

class Action(object):
	"""
	Base class
	TODO: abs
	"""
	@classmethod
	def run(cls, game_manager):
		"""
		Make the action happen
		:type game_manager: GameManager
		"""
		raise NotImplementedError()

class Reverse(Action):
	@classmethod
	def run(cls, game_manager):
		game_manager.change_direction()