#!/usr/bin/env python
"""
credit to: https://github.com/bueda/tornado-boilerplate
"""
from tornado import web, ioloop, httpserver
from tornado.options import options

from app import CardGameApplication

def main():
	app = CardGameApplication()
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port)
	ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass