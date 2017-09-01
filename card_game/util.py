"""
Utility classes
"""
import constants

__all__ = ["Logger"]

class Logger(object): # pragma: no cover
	@staticmethod
	def debug(msg, tag=constants.DEFAULT_TAG):
		if constants.DEBUG:
			print "[{}] {}".format(tag, msg)
