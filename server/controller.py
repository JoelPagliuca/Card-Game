"""
"""
import uuid
import logging
import threading

from util import WebSocketInterface

from card_game.engine import GameManager
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECK

__all__ = ["GameController", "GameThread"]

class GameThread(threading.Thread):
	"""
	Thread for running the game, note the game and controller
	"""
	def __init__(self, game, controller):
		super(GameThread, self).__init__()
		self._game = game
		self._controller = controller
	
	def run(self):
		results = self._game.run()
		self._controller.finish_game(results)

class GameController(object):
	"""deals with the game and provides a nicer interface for the WebSocket view"""
	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self._game = None
		self.players = []
		self.max_players = int(kwargs.get("max_players", 3))
		self.clients = {}		# Player -> Handler
		logging.info("created GameController for game "+self.id+", now waiting for {} connections".format(str(self.max_players)))

	def add_player(self, player, client):
		"""
		add player to the controller, will start the game if max_players hit

		:param player: the player to add
		:param client: the client for the player
		"""
		self.players.append(player)
		self.clients[player.id] = client
		logging.info(self.id+" adding "+player.name+", now at "+str(len(self.players))+" players")
		if len(self.players) >= self.max_players:
			logging.info("Got enough player connections, starting a game")
			self.start_game()
	
	def start_game(self):
		logging.info("Starting game "+self.id)
		self._game = GameManager(self.players, GET_DECK(), RULES)
		self._game.interface = WebSocketInterface
		for _, client in self.clients.items():
			self._game.observe(client)	# FIXME do real observer pattern, client.observe(observable)
		game_thread = GameThread(self._game, self)
		game_thread.start()
	
	def stop_game(self):
		logging.info("Stopping game "+self.id)
		# remove all players, close their connections, kill the game
		self.players[:] = []
		for player in self.clients:
			self._game.deleteObserver(self.clients[player])
			self.clients[player].close()	# FIXME write out a GAME_OVER message to the client
		self.clients.clear()
		self._game.running = False
	
	def finish_game(self, results):
		"""
		End game gracefully because of a win

		:param dict results: final game context from the game manager
		"""
		for _, client in self.clients.iteritems():
			client.game_end(results)
		self.stop_game()