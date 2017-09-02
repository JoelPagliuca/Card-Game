#!/usr/bin/env python
"""
credit to: https://github.com/bueda/tornado-boilerplate
"""
from os.path import dirname as dir
from sys import path
path.append(dir(path[0]))
import card_game # FIXME: 11/10 hack

from tornado import web, ioloop
from tornado.options import options

from settings import settings
from urls import url_patterns

class CardGameApplication(web.Application):
	def __init__(self):
		web.Application.__init__(self, url_patterns, **settings)

def main():
	app = CardGameApplication()
	app.listen(options.port)
	ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass