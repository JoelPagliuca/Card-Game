"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
All actions will be given pointers to the card and game_manager
Assume that the current player is who played the card with the action
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
		player = game_manager.current_player()
		player.hand.remove(self.card)
		game_manager.pile.play_card(self.card)

class DrawCard(Action):
	def run(self, game_manager):
		"""
		Make the action happen
		:type game_manager: GameManager
		"""
		top_card = game_manager.deck.draw_card()
		game_manager.current_player().take_card(top_card)

class Reverse(PlayCard):
	def run(self, game_manager):
		super(Reverse, self).run(game_manager)
		game_manager.change_direction()
