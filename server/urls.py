"""
URL routing for the application
"""
from handlers.hello import HelloHandler

url_patterns = [
	(r"/hello", HelloHandler),
]