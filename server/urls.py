"""
URL routing for the application
"""
from handlers.hello import HelloHandler
from handlers.gameview import GameViewHandler
from handlers.gamecreate import GameCreateHandler

url_patterns = [
	(r"/hello", HelloHandler),
	(r"/gamecreate", GameCreateHandler),
	(r"/gameview", GameViewHandler),
]