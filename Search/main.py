from tree_search import Tree
import time

tree = Tree()
curr = time.time()
print(tree.search(1, 0))
print(time.time() - curr)
print(len(tree.visited))