"""
Hello-world request handler
"""
from base import BaseHandler

__all__ = ["HelloHandler"]

class HelloHandler(BaseHandler):
	def get(self):
		self.write("""{
			"msg": "Hello, This is a server response"
		}
		""")