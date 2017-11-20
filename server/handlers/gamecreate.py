"""
"""
import logging

from server.controller import GameController
from server.data import GAMES

from tornado.web import RequestHandler

__all__ = ["GameCreateHandler"]


class GameCreateHandler(RequestHandler):
	"""Handler for creating games"""
	def post(self):
		"""
		create a new GameController
		"""
		num_players = self.get_body_argument("number_players", 3)
		logging.info("going to make a game with "+str(num_players)+" players")
		controller = GameController(max_players=num_players)
		GAMES[controller.id] = controller
		create_response = {
			"game_id": controller.id
		}
		self.write(create_response)
	
	def check_xsrf_cookie(self):
		return True # FIXME have a cleaner interface to this handler