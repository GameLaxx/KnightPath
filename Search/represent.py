import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def bitboard_to_matrix(board, position):
    matrix = np.zeros((8, 8), dtype=int)
    for i in range(64):
        row, col = divmod(i, 8)
        if i == position:
            matrix[row][col] = 2
        elif board & (1 << i):
            matrix[row][col] = 1
        else:
            matrix[row][col] = 0
    return matrix

def plot_board(board, position):
    matrix = bitboard_to_matrix(board, position) # create matrix
    # create cmap for coloring
    plt.figure(figsize=(6, 6))
    cmap = plt.cm.get_cmap('viridis', 3)
    im = plt.imshow(matrix, cmap=cmap, origin='upper')
    # add colors according to matrix
    for i in range(8):
        for j in range(8):
            value = matrix[i, j]
            plt.text(j, i, str(value), ha='center', va='center', color='white' if value else 'black')
    # plot
    plt.title("Cavalouuuu")
    plt.xticks(range(8))
    plt.yticks(range(8))
    plt.grid(False)
    plt.colorbar(im, ticks=[0, 1, 2], label="Square state")
    plt.show()

def animate_bitboards(frames, interval=300, save_path=None):
    # create plot
    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.cm.get_cmap('viridis', 3)
    mat = ax.imshow(np.zeros((8, 8)), cmap=cmap, vmin=0, vmax=2)
    # labels
    text_labels = [[ax.text(j, i, '', ha='center', va='center') for j in range(8)] for i in range(8)]
    # update function of the animation
    def update(frame):
        board, position = frame
        matrix = bitboard_to_matrix(board, position)
        mat.set_data(matrix)
        for i in range(8):
            for j in range(8):
                val = matrix[i, j]
                text_labels[i][j].set_text(str(val) if val != 0 else "")
                text_labels[i][j].set_color('white' if val == 1 or val == 2 else 'black')
        return [mat] + [label for row in text_labels for label in row]
    # create animation
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
    # save it
    if save_path:
        if save_path.endswith('.gif'):
            ani.save(save_path, writer='pillow')
        else:
            ani.save(save_path, writer='ffmpeg')
    # set titles
    plt.title("Cavalouuuuu")
    plt.xticks(range(8))
    plt.yticks(range(8))
    plt.show()