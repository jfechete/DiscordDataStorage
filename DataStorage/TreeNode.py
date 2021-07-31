import uuid
class TreeNode:
    """Base tree node class that can store data in a seperate file. Meant to be inherited from."""
    
    def __init__(self):
        self.uuid = str(uuid.uuid4())