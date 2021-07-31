import uuid

NODE_FILE_EXTENSION = ".dstn"
DATA_FILE_EXTENSION = ".dstd"

class TreeNode:
    """Base tree node class that can store data in a seperate file. Meant to be inherited from."""
    
    def __init__(self):
        """Creates a new tree node (make sure to add it to a tree)"""
        self.uuid = str(uuid.uuid4())

        self._data_uuid = str(uuid.uuid4())

        #don't think I'll need parent or root nodes within the node, I'll add them here if I do
        self._left_child_uuid = None
        self._right_child_uuid = None

    @classmethod
    def get_node(cls, uuid):
        """Reads a node from disk with the given uuid"""
        pass

    def _save_node(self):
        """called automatically after editing node properties"""

    def get_data(self):
        """gets the data saved in this node"""
        pass
    
    def set_data(self,data):
        """overwrites this node's data"""
        pass