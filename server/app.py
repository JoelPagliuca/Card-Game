from tornado import web
from tornado.options import options

from settings import settings
from urls import url_patterns

class CardGameApplication(web.Application):
	def __init__(self):
		web.Application.__init__(self, url_patterns, **settings)
