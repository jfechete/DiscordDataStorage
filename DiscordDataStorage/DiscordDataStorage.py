import TreeNode

if __name__ == "__main__":
    #test stuff here
    node0 = TreeNode.TreeNode(0)
    node1a = TreeNode.TreeNode(1)
    node1b = TreeNode.TreeNode(1)
    node2 = TreeNode.TreeNode(2)
    print(node1a == 1)
    print(node1a > 0)
    print(node1a < 0)
    print(node1a == node1b)
    print(node1a > node0)
    print(node1a < node0)
    print(node1a > node2)
    print(node1a < node2)
    print(node1a != node2)
    print(node1a != node1b)