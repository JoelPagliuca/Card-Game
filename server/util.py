"""Just some classes I couldn't find a better place for"""
from server.data import CLIENTS, ACTION

from card_game.engine import TextInterface

import logging
import time

__all__ = ["WebSocketInterface"]

class WebSocketInterface(TextInterface):
	"""
	Gets user input over WebSocket
	"""
	@classmethod
	def render(cls, msg):
		pass
	
	@classmethod
	def get_input(cls, prompt=None, player=None):
		"""
		gets a string from the user
		wait for string from the WebSocket client
		:type prompt: str
		:rtype: str
		"""
		logging.debug("Taking input from "+player.name)
		client = CLIENTS[player]
		while True:
			if client.input:
				output = client.input
				client.input = None
				return output
			time.sleep(0.1)
	
	@classmethod
	def get_choice(cls, options, prompt="", player=None):
		"""
		get a choice from a user. 
		expecting '{"input": "action.id"}' from the user

		:param options: list of descriptions to present to the user
		:type options: list(:class:`card_game.action.Action`)
		:return: the item chosen from the list
		:rtype: Action
		"""
		actions_dict, client_data = {}, {}		# this will be {action.id:action}
		game_client = CLIENTS[player]
		for action in options:
			actions_dict[action.id] = action.toDict()
		client_data.update({"action": ACTION.OPTION})
		client_data.update(actions_dict)
		game_client.write_message(client_data)
		choice = -1
		while not choice in actions_dict.keys():
			choice = cls.get_input(prompt, player)
		# find the choice mapping to this id
		return cls._get_option_with_id(choice, options)
	
	@classmethod
	def _get_option_with_id(cls, id_, options):
		for o in options:
			if o.id == id_:
				return o