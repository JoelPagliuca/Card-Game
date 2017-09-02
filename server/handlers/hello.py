"""
Hello-world request handler
"""
import logging

from base import BaseHandler

__all__ = ["HelloHandler"]

class HelloHandler(BaseHandler):
	def open(self):
		self.write_message({'msg': 'hello'})
	def on_message(self, message):
		logging.info("Received message: " + message)
	def on_close(self):
		pass