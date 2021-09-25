#Modules
import uuid
import os
import json

#Constants
NODE_FILE_EXTENSION = ".dstn"
DATA_FILE_EXTENSION = ".dstd"
DEFAULT_DATA_DIR_NAME = "Data"

#Data keys
UUID_KEY = "uuid"
DATA_UUID_KEY = "data_uuid"
LEFT_NODE_KEY = "left_child"
RIGHT_NODE_KEY = "right_child"
ID_KEY = "id"

#Variables
data_dir = os.path.join(os.path.split(__file__)[0],DEFAULT_DATA_DIR_NAME)
_initialized = False

#Main class
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
        _init()
        data = cls._get_node_data(uuid)
        uuid = data[UUID_KEY]
        data_uuid = data[DATA_UUID_KEY]
        left_node = data[LEFT_NODE_KEY]
        right_node = data[RIGHT_NODE_KEY]
        id = data[ID_KEY]
        return cls._constructor(uuid, data_uuid, id, left_node, right_node)

    @classmethod
    def _get_node_data(cls, uuid):
        with open(os.path.join(data_dir,uuid + "." + NODE_FILE_EXTENSION),"r") as node_file:
            data = json.load(node_file)
        return data


    @classmethod
    def _constructor(cls, uuid, data_uuid, id, left_child = None, right_child = None, self = None):
        _init()
        if self == None:
            self = cls.__new__(cls)

        self.uuid = uuid
        self._data_uuid = data_uuid
        self.id = id
        #don't think I'll need parent or root nodes within the node, I'll add them here if I do
        self._left_child_uuid = left_child
        self._right_child_uuid = right_child

        return self

    def get_data(self):
        """gets the data saved in this node"""
    
    def set_data(self,data):
        """overwrites this node's data"""

    def get_child(self, id):
        """gets the child node with the passed id"""
        if self.id == id:
            return self
        elif self.id < id:
            if self._right_child_uuid == None:
                raise ValueError("Child not found")
            return self._get_child(self._right_child_uuid).get_child(id)
        else:
            if self._left_child_uuid == None:
                raise ValueError("Child not found")
            return self._get_child(self._left_child_uuid).get_child(id)

    def add_child(self, child):
        """adds a child node to this tree"""
        if self == child:
            raise ValueError("Child already has same id in tree")
        if self < child:
            if self._right_child_uuid == None:
                self._right_child_uuid = child.uuid
                self._save_node()
            else:
                self._get_child(self._right_child_uuid).add_child(child)
        else:
            if self._left_child_uuid == None:
                self._left_child_uuid = child.uuid
                self._save_node()
            else:
                self._get_child(self._left_child_uuid).add_child(child)

    def del_child(self, id, parent = None, parent_side = None):
        right_child = None if self._right_child_uuid == None else self._get_child(self._right_child_uuid)
        left_child = None if self._left_child_uuid == None else self._get_child(self._left_child_uuid)
        if self.id == id:
            if right_child == None and left_child == None:
                if parent == None:
                    pass #TODO: design empty tree structure
                else:
                    if parent_side > 0:
                        parent._right_child_uuid = None
                    else:
                        parent._left_child_uuid = None
                    parent._save_node()
            elif right_child == None or left_child == None:
                child = right_child or left_child #TODO: design solution for when root is deleted (root may be referenced by other objects, can't change it)
                if parent_side > 0:
                    parent._right_child_uuid = child.uuid
                else:
                    parent._left_child_uuid = child.uuid
                parent._save_node()
            self._del_data()
        else:
            if self.id < id:
                right_child.del_child(id, self, 1)
            else:
                left_child.del_child(id, self, -1)
    
    def _del_data(self):
        pass

    def str_tree(self, first_start = "", body_start = ""):
        """gets a string representation of this node and it's children"""
        str_self = first_start + str(self)
        left_child = self._get_child(self._left_child_uuid)
        str_left_child = (left_child.str_tree(body_start + "├", body_start + "│") if left_child else body_start + "├" + str(left_child))
        right_child = self._get_child(self._right_child_uuid)
        str_right_child = (right_child.str_tree(body_start + "└", body_start + " ") if right_child else body_start + "└" + str(right_child))
        return "\n".join((str_self,str_left_child,str_right_child))

    def __str__(self):
        return str(self.id)

    def __eq__(self,other):
        if isinstance(other,TreeNode):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            return NotImplemented
    
    def __lt__(self,other):
        if isinstance(other, TreeNode):
            return self.id < other.id
        elif isinstance(other, int):
            return self.id < other
        else:
            return NotImplemented

    def __ne__(self,other):
        eq = self.__eq__(other)
        return not eq if eq != NotImplemented else eq

    def __gt__(self, other):
        lt = self.__lt__(other)
        return not lt if lt != NotImplemented else lt
    
    def __le__(self,other):
        lt = self.__lt__(other)
        eq = self.__eq__(other)
        if lt == NotImplemented or eq == NotImplemented:
            return NotImplemented
        return lt or eq

    def __ge__(self,other):
        gt = self.__gt__(other)
        eq = self.__eq__(other)
        if gt == NotImplemented or eq == NotImplemented:
            return NotImplemented
        return gt or eq
        
    def _save_node(self):
        """called automatically after editing node properties, overwrites the node file to reflect changes"""
        with open(os.path.join(data_dir,self._get_node_file_name()),"w") as node_file:
            json.dump(self._get_node_save_data(),node_file)

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

    def _get_child(self, child):
        if child == None:
            return None
        return self.__class__.get_node(child)

#Methods
def set_data_dir(dir):
    global data_dir
    data_dir = dir

def _init():
    global _initialized
    if _initialized:
        return
    if data_dir != os.path.join(os.path.split(__file__)[0],DEFAULT_DATA_DIR_NAME) and not os.path.isdir(data_dir): # TODO: Test if this works
        os.mkdir(data_dir)
    _initialized = True