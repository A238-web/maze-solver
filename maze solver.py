
import tkinter as tk
from collections import deque

maze = [
    "S...#...",
    ".#..#...",
    ".#......",
    "...##...",
    "....#..E"
]

root = tk.Tk()
root.title("Maze Solver")

cell = 50
canvas = tk.Canvas(root, width=400, height=250)
canvas.pack()

start = (0, 0)
end = (4, 7)
boxes = {}

def draw():
    for r in range(5):
        for c in range(8):
            color = "white"
            if maze[r][c] == "#":
                color = "black"
            if (r, c) == start:
                color = "green"
            if (r, c) == end:
                color = "red"

            boxes[(r, c)] = canvas.create_rectangle(
                c*cell, r*cell, (c+1)*cell, (r+1)*cell,
                fill=color, outline="gray"
            )

def solve(bfs):
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft() if bfs else queue.pop()

        if current == end:
            break

        r, c = current
        for nxt in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
            x, y = nxt
            if (0 <= x < 5 and 0 <= y < 8
                and maze[x][y] != "#"
                and nxt not in visited):
                visited.add(nxt)
                parent[nxt] = current
                queue.append(nxt)

    if end not in visited:
        return [], []

    path = []
    p = end
    while p != start:
        path.append(p)
        p = parent[p]
    path.append(start)
    path.reverse()

    return list(visited), path

def run(bfs):
    visited, path = solve(bfs)
    steps = visited + path

    def show(i):
        if i == len(steps):
            return

        p = steps[i]
        if p not in (start, end):
            color = "yellow" if i >= len(visited) else "lightblue"
            canvas.itemconfig(boxes[p], fill=color)

        root.after(150, lambda: show(i+1))

    show(0)

draw()

tk.Button(root, text="BFS", command=lambda: run(True)).pack()
tk.Button(root, text="DFS", command=lambda: run(False)).pack()

root.mainloop()
