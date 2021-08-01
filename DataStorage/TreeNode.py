import uuid
import os
import json

NODE_FILE_EXTENSION = ".dstn"
DATA_FILE_EXTENSION = ".dstd"
DEFAULT_DATA_DIR_NAME = "Data"

data_dir = os.path.join(os.path.split(__file__)[0],DEFAULT_DATA_DIR_NAME)

class TreeNode:
    """Base tree node class that can store data in a seperate file. Meant to be inherited from."""
    
    def __init__(self):
        """Creates a new tree node (make sure to add it to a tree)"""
        TreeNode._constructor(str(uuid.uuid4()),str(uuid.uuid4()),self = self)

    @classmethod
    def get_node(cls, uuid):
        """Reads a node from disk with the given uuid"""
        with open(os.path.join(data_dir,uuid + "." + NODE_FILE_EXTENSION),"r") as node_file:
            pass

    @classmethod
    def _constructor(cls, uuid, data_uuid, left_child = None, right_child = None, self = None):
        if self == None:
            self = cls.__new__(cls)

        self.uuid = uuid
        self._data_uuid = data_uuid
        #don't think I'll need parent or root nodes within the node, I'll add them here if I do
        self._left_child_uuid = left_child
        self._right_child_uuid = right_child

        self._save_node()
        self.set_data(None)

        return self

    def _save_node(self):
        """called automatically after editing node properties, overwrites the node file to reflect changes"""
        with open(os.path.join(data_dir,self._get_node_file_name()),"w") as node_file:
            node_file.write(self._get_node_save_text())

    def get_data(self):
        """gets the data saved in this node"""
    
    def set_data(self,data):
        """overwrites this node's data"""

    def _get_node_file_name(self):
        return self.uuid + "." + NODE_FILE_EXTENSION

    def _get_node_save_text(self): #separate method so child classes can append to
        save_text = "{},{}\n".format(self.uuid,self._data_uuid)
        save_text += "{},{}".format(self._left_child_uuid if self._left_child_uuid != None else "",
                                    self._right_child_uuid if self._right_child_uuid != None else "")
        return save_text

def set_data_dir(dir):
    global data_dir
    data_dir = dir

def _init():
    if not os.path.isdir(data_dir): # TODO: make this only trigger when data is written and default directory is used, so it doesn't make the folder if a different directory is set
        os.mkdir(data_dir)

_init()