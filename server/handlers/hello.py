"""
Hello-world request handler
"""
from base import BaseHandler

__all__ = ["HelloHandler"]

class HelloHandler(BaseHandler):
	def open(self):
		self.write_message({'msg': 'hello'})
	def on_close(self):
		pass