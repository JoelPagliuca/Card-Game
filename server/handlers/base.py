import json
from tornado import websocket

__all__ = ["BaseHandler"]

class BaseHandler(websocket.WebSocketHandler):
	"""
	Contains all common handler methods
	all other handlers should subclass this one.
	"""
	def check_origin(self, origin):
		"""
		FIXME don't let every origin maybe
		"""
		return True
