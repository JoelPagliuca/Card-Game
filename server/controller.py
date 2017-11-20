"""
"""
import uuid
import logging
import threading

from util import WebSocketInterface

from card_game.engine import GameManager
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECK

__all__ = ["GameController"]

class GameController(object):
	"""deals with the game and provides a nicer interface for the WebSocket view"""
	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self._game = None
		self.players = []
		self.max_players = kwargs.get("max_players", 3)
		self.clients = {}		# Player -> Handler
		logging.info("created GameController for game "+self.id)
	
	def start_game(self):
		self._game = GameManager(self.players, GET_DECK(), RULES)
		self._game.interface = WebSocketInterface
		for _, client in self.clients.items():
			self._game.observe(client)	# FIXME do real observer pattern, client.observe(observable)
		logging.info("Starting game "+self.id)
		game_thread = threading.Thread(target=self._game.run)
		game_thread.start()
	
	def stop_game(self):
		pass