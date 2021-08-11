import uuid
import os
import json

NODE_FILE_EXTENSION = ".dstn"
DATA_FILE_EXTENSION = ".dstd"
DEFAULT_DATA_DIR_NAME = "Data"

#Data keys
UUID_KEY = "uuid"
DATA_UUID_KEY = "data_uuid"
LEFT_NODE_KEY = "left_child"
RIGHT_NODE_KEY = "right_child"
ID_KEY = "id"

data_dir = os.path.join(os.path.split(__file__)[0],DEFAULT_DATA_DIR_NAME)

class TreeNode:
    """Base tree node class that can store data in a seperate file. Meant to be inherited from."""
    
    def __init__(self, id):
        """Creates a new tree node (make sure to add it to a tree)"""
        TreeNode._constructor(str(uuid.uuid4()),str(uuid.uuid4()),id,self = self)
        self._save_node()
        self.set_data(None)

    @classmethod
    def get_node(cls, uuid):
        """Reads a node from disk with the given uuid"""
        with open(os.path.join(data_dir,uuid + "." + NODE_FILE_EXTENSION),"r") as node_file:
            data = json.load(node_file)
        uuid = data[UUID_KEY]
        data_uuid = data[DATA_UUID_KEY]
        left_node = data[LEFT_NODE_KEY]
        right_node = data[RIGHT_NODE_KEY]
        id = data[ID_KEY]
        return cls._constructor(uuid, data_uuid, id, left_node, right_node)

    @classmethod
    def _constructor(cls, uuid, data_uuid, id, left_child = None, right_child = None, self = None):
        if self == None:
            self = cls.__new__(cls)

        self.uuid = uuid
        self._data_uuid = data_uuid
        self.id = id
        #don't think I'll need parent or root nodes within the node, I'll add them here if I do
        self._left_child_uuid = left_child
        self._right_child_uuid = right_child

        return self

    def _save_node(self):
        """called automatically after editing node properties, overwrites the node file to reflect changes"""
        with open(os.path.join(data_dir,self._get_node_file_name()),"w") as node_file:
            json.dump(self._get_node_save_data(),node_file)

    def get_data(self):
        """gets the data saved in this node"""
    
    def set_data(self,data):
        """overwrites this node's data"""

    def _get_node_file_name(self):
        return self.uuid + "." + NODE_FILE_EXTENSION

    def _get_node_save_data(self): #separate method so child classes can edit it
        save_data = {}
        save_data[UUID_KEY] = self.uuid
        save_data[DATA_UUID_KEY] = self._data_uuid
        save_data[LEFT_NODE_KEY] = self._left_child_uuid
        save_data[RIGHT_NODE_KEY] = self._right_child_uuid
        save_data[ID_KEY] = self.id
        return save_data

    def __str__(self):
        return str(self.id)

    def str_tree(self, first_start = "", body_start = ""): # TODO: test more after adding child_add method
        """gets a string representation of this node and it's children"""
        str_self = first_start + str(self)
        left_child = self.get_child(self._left_child_uuid)
        str_left_child = body_start + (left_child.str_tree(body_start + "├", body_start + "│") if left_child else "├" + str(left_child))
        right_child = self.get_child(self._right_child_uuid)
        str_right_child = body_start + (right_child.str_tree(body_start + "└", body_start + " ") if right_child else "└" + str(right_child))
        return "\n".join((str_self,str_left_child,str_right_child))

    def get_child(self, child):
        if child == None:
            return None
        return self.__class__.get_node(child)

def set_data_dir(dir):
    global data_dir
    data_dir = dir

def _init():
    if not os.path.isdir(data_dir): # TODO: make this only trigger when data is written and default directory is used, so it doesn't make the folder if a different directory is set
        os.mkdir(data_dir)

_init()