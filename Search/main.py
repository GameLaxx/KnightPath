from tree_search import Node, Tree
import time
start_node = Node(1, 0)
tree = Tree(start_node)
curr = time.time()
print(tree.launch_search())
print(time.time() - curr)
print(len(tree.visited))