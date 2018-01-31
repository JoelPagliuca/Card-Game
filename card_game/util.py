"""
Utility classes
"""
import constants

__all__ = ["abstractclassmethod"]

class abstractclassmethod(classmethod):
	"""combines the two decorators"""

	__isabstractmethod__ = True

	def __init__(self, callable):
		callable.__isabstractmethod__ = True
		super(abstractclassmethod, self).__init__(callable)

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