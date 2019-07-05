import collections

class StrDictKey(collections.UserDict):

	def __missing__(self, key):
		if isinstance(key, str):
			raise KeyError
		return self[str(key)]

	def __contains__(self, key):
		return str(key) in self.data

	def __setitem__(self, key, item):
		self.data[str(key)] = item