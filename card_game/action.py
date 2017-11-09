"""
An effect on a card, this is how stuff like Reverse and Skip will be implemented
All actions will be given pointers to the card and game_manager
Assume that the current player is who played the card with the action
"""
__all__ = ["PlayCard", "DrawCard", "Reverse"]

class Action(object):
	TAG = "ACTION"
	def __init__(self, card):
		self.card = card
		self.id = id(self)
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

	def toDict(self):
		"""
		Convert to JSON string
		:rtype: dict
		"""
		output = { "action": self.TAG }
		if self.card:
			output["card"] = self.card.toDict()
		return output

class PlayCard(Action):
	TAG = "PLAY"
	"""
	Just play the card
	"""
	def run(self, game_manager):
		player = game_manager.current_player()
		player.hand.remove(self.card)
		game_manager.pile.play_card(self.card)

class DrawCard(Action):
	TAG = "DRAW"
	def run(self, game_manager):
		"""
		Make the action happen
		:type game_manager: GameManager
		"""
		top_card = game_manager.deck.draw_card()
		game_manager.current_player().take_card(top_card)

class Reverse(PlayCard):
	TAG = "REVERSE"
	def run(self, game_manager):
		super(Reverse, self).run(game_manager)
		game_manager.change_direction()
