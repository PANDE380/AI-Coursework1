import matplotlib.pyplot as plt
from collections import deque

# Maze: 0 = free cell, 1 = wall
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
] 

start = (0, 0)
goal = (4, 4)

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return path[::-1]  # Return reversed path

        r, c = node
        for dr, dc in [(0,1),(1,0),(-1,0),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                queue.append((nr, nc))
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
    return None

path = bfs(maze, start, goal)
print("BFS Path:", path)

# Visualization
def draw_maze(maze, path=None):
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap='binary')
    if path:
        x, y = zip(*path)
        ax.plot(y, x, marker='o', color='red')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

draw_maze(maze, path)
