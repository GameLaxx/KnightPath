def represent_board(board, position):
    ret = "."
    for i in range(64):
        if i % 8 == 0 and i != 0:
            ret += "\n."
        if i == position :
            ret += "2"
        elif board & 1 << i:
            ret += "1"
        else:
            ret += "0"
        ret += "."
    return ret

class Node():
    def __init__(self, board, position, parent = None):
        self.board = board
        self.position = position
        self.childs = []
        self.parent = parent

    def generate_childs(self):
        current_square = divmod(self.position, 8)
        for delta in [6, 15, 10, 17, -6, -15, -10, -17]:
            new_position = self.position + delta
            if not (0 <= new_position < 64): # not on the board
                continue
            wanted_square = divmod(new_position, 8)
            if not (abs(wanted_square[0] - current_square[0]) <= 2 and abs(wanted_square[1] - current_square[1]) <= 2): # not around the knight
                continue
            if self.board & 1 << new_position != 0: # already been there
                continue
            self.childs.append(Node(self.board | 1 << new_position, new_position, self))

    def __repr__(self):
        return represent_board(self.board, self.position)
                               
class Tree():
    def __init__(self, start_node):
        self.start_node = start_node
        self.visited = {}
        self.total_searchs = 0

    def __search(self, current_node : Node):
        self.total_searchs += 1
        if self.total_searchs > 1_000_000:
            return None
        if current_node.board == 0xFFFFFFFFFFFFFFFF: #complete
            return current_node
        if current_node.board in self.visited and current_node.position in self.visited[current_node.board] and not self.visited[current_node.board][current_node.position]:
            return None # already seen and failed
        current_node.generate_childs()
        for child in current_node.childs:
            ret_search = self.__search(child)
            if ret_search: # found complete
                return ret_search
        # no child is worth
        if current_node.board not in self.visited:
            self.visited[current_node.board] = {}
        self.visited[current_node.board][current_node.position] = False
        return None
        
    def launch_search(self):
        return self.__search(self.start_node)