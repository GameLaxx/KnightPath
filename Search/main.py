from tree_search import Tree
from represent import animate_bitboards
import time

tree = Tree()
curr = time.time()
ret = tree.search(1, 0)
print(time.time() - curr)
print(len(tree.visited))
animate_bitboards(ret, save_path="cavalou.gif")