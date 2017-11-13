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

# didn't work, id wasn't set on the subclasses
# class GameObject(object):
# 	"""
# 	Object that can be converted to JSON and has an ID
# 	"""
# 	fields = ('id',)
# 	def __init__(self):
# 		self.id = 5
# 	def toDict(self):
# 		return {f:getattr(self, f) for f in self.fields}