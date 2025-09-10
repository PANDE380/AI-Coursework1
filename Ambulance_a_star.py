
import heapq

# Grid legend:
# 0 -> free cell, cost to enter = 1
# 1 -> obstacle (not passable)
# 2 -> traffic/heavy road (cost to enter = 5)

grid = [
    [0, 0, 0, 0, 0],
    [0, 2, 1, 2, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 2, 0],
]

ROWS = len(grid)
COLS = len(grid[0])

start = (0, 0)         # ambulance location (row, col)
goal = (4, 3)          # patient location (row, col)

# movement directions: up, down, left, right
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def passable(r, c):
    return grid[r][c] != 1  # 1 is obstacle

def move_cost(r, c):
    """Cost to ENTER cell (r,c). Adjust to model traffic or road speed."""
    cell = grid[r][c]
    if cell == 0:
        return 1
    if cell == 2:
        return 5
    return 1

def heuristic(a, b):
    """Manhattan distance heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    # Priority queue items: (f_score, g_score, node)
    pq = []
    heapq.heappush(pq, (heuristic(start, goal), 0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while pq:
        f, g, current = heapq.heappop(pq)

        if current == goal:
            # reconstruct path
            path = []
            node = current
            while node:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path, g_score[current]

        for dr, dc in dirs:
            nr, nc = current[0] + dr, current[1] + dc
            if not in_bounds(nr, nc) or not passable(nr, nc):
                continue

            tentative_g = g_score[current] + move_cost(nr, nc)
            neighbor = (nr, nc)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(pq, (f_score, tentative_g, neighbor))

    return None, float('inf')  # no path found

def print_grid_with_path(path):
    # Print grid with path marked as 'P', start 'S', goal 'G', obstacle '#', traffic 'T', free '.'
    path_set = set(path) if path else set()
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            if (r, c) == start:
                ch = 'S'
            elif (r, c) == goal:
                ch = 'G'
            elif (r, c) in path_set:
                ch = 'P'
            elif grid[r][c] == 1:
                ch = '#'
            elif grid[r][c] == 2:
                ch = 'T'
            else:
                ch = '.'
            line.append(ch)
        print(' '.join(line))
    print()

if __name__ == "__main__":
    solution_path, total_cost = a_star(start, goal)
    if solution_path:
        print("Start:", start)
        print("Goal:", goal)
        print("Path found (row,col):", solution_path)
        print("Total travel cost:", total_cost)
        print("\nGrid legend: S=start, G=goal, P=path, #=obstacle, T=traffic, .=free")
        print_grid_with_path(solution_path)
    else:
        print("No path found from", start, "to", goal)
