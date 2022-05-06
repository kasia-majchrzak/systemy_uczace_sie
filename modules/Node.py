class Node:
	@property
	def label(self):
		return self._label

	@label.setter
	def label(self, value):
		self._label = value

	@property
	def isLeaf(self):
		return self._isLeaf

	@isLeaf.setter
	def isLeaf(self, value):
		self._isLeaf = value

	@property
	def children(self):
		return self._children

	@children.setter
	def children(self, value):
		self._children = value

	@property
	def decision(self):
		return self._decision

	@decision.setter
	def decision(self, value):
		self._decision = value

	def __init__(self,isLeaf, label):
		self._label = label
		self._isLeaf = isLeaf
		self._children = []
		self._decision = ''