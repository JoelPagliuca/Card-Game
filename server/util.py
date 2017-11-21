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
	_TAG = "WS_IFACE"
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
		logging.debug("Taking input from "+player.name, cls._TAG)
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
		actions = {}		# this will be {action.id:action}
		data = {}
		client = CLIENTS[player]
		for action in options:
			actions[action.id] = action.toDict()
		data.update({"action": ACTION.OPTION})
		data.update(actions)
		client.write_message(data)
		choice = -1
		while not choice in actions.keys():
			choice = cls.get_input(prompt, player)
			# find the choice mapping to this id
			for o in options:
				if o.id == choice:
					return o
			continue