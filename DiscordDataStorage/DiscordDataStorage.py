import TreeNode
import random

if __name__ == "__main__":
    #test stuff here
    """values = list(range(32))
    random.shuffle(values)
    root = TreeNode.TreeNode(values.pop(0))
    for id in values:
        root.add_child(TreeNode.TreeNode(id))
    print(root.uuid)
    print(root.str_tree())"""
    root = TreeNode.TreeNode.get_node("0dfc638b-0add-4533-bc14-66c2ee758e43")
    print(root.str_tree())
    print(root.get_child(25).str_tree())
    root.del_child(24)
    print(root.get_child(25).str_tree())