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

precomputed_coords = [(i // 8, i % 8) for i in range(64)]
                               
class Tree():
    def __init__(self):
        self.visited = set()        
        self.total_searchs = 0
        
    def generate_new_positions(self, board, position):
        ret = []
        current_square = precomputed_coords[position]
        for delta in [6, 15, 10, 17, -6, -15, -10, -17]:
            new_position = position + delta
            if not (0 <= new_position < 64): # not on the board
                continue
            wanted_square = precomputed_coords[new_position]
            if not (abs(wanted_square[0] - current_square[0]) <= 2 and abs(wanted_square[1] - current_square[1]) <= 2): # not around the knight
                continue
            if board & 1 << new_position != 0: # already been there
                continue
            ret.append((board | 1 << new_position, new_position, self))
        return ret

    def search(self, current_board, current_position):
        self.total_searchs += 1
        if self.total_searchs > 100_000:
            return None
        if current_board == 0xFFFFFFFFFFFFFFFF: #complete
            return [current_board]
        if (current_board, current_position) in self.visited:
            return None # already seen and failed
        next_positions = self.generate_new_positions(current_board, current_position)
        next_positions.sort(key = lambda pos : sum(1 for _ in self.generate_new_positions(pos[0] | (1 << pos[1]), pos[1])))
        for next in next_positions:
            ret_search = self.search(next[0], next[1])
            if ret_search: # found complete
                return [current_board] + ret_search
        # no child is worth
        self.visited.add((current_board, current_position))
        return None