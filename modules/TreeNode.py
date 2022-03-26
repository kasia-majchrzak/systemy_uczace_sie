from idlelib.tree import TreeNode


class TreeNodeDTO(TreeNode):
    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value

    @property
    def entrophy(self):
        return self._entrophy

    @entrophy.setter
    def entrophy(self, value):
        self._entrophy = value

    def __init__(self, data, level: int = 0, parent: TreeNode = None):
        super().__init__()
        self.item = data
        self.level = level
        self.parent = parent

