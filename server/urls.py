"""
URL routing for the application
"""
from handlers.hello import HelloHandler
from handlers.gameview import GameViewHandler

url_patterns = [
	(r"/hello", HelloHandler),
	(r"/gameview", GameViewHandler),
]