"""
"""
import uuid



__all__ = ["GameController"]

class GameController(obkect):
	"""deals with the game and provides a nicer interface for the WebSocket view"""
	def __init__(self):
		self.id = str(uuid.uuid4())
		self._game = None
		self.players = []
		self.clients = {}		# Player -> Handler
	
	def start_game(self):
		pass
	
	def stop_game(self):
		pass