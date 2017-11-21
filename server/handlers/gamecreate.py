"""
"""
import logging

from server.controller import GameController
from server import data

from tornado.web import RequestHandler

__all__ = ["GameCreateHandler"]


class GameCreateHandler(RequestHandler):
	"""Handler for creating games"""
	def post(self):
		"""
		create a new GameController
		"""
		try:
			num_players = int(self.get_body_argument("number_players", 3))
			assert(num_players >= 1)
		except:
			logging("couldn't get a valid number_players from client")
		logging.info("going to make a game with "+str(num_players)+" players")
		controller = GameController(max_players=num_players)
		data.GAMES[controller.id] = controller
		create_response = {
			"game_id": controller.id
		}
		self.write(create_response)
	
	def check_xsrf_cookie(self):
		return True # FIXME have a cleaner interface to this handler