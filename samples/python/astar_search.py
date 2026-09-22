#!/usr/bin/env python
"""
A* (A-star) search on a 2D grid.

The grid is a list of strings where '.' is free, '#' is a wall,
'S' is the start and 'G' is the goal. Movement is 4-directional
with unit cost and the Manhattan distance heuristic.

Usage:
	python astar_search.py            # runs the built-in demo
"""

import heapq
from itertools import count


def manhattan(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid, node):
	rows, cols = len(grid), len(grid[0])
	r, c = node
	for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
		nr, nc = r + dr, c + dc
		if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
			yield (nr, nc)


def astar(grid, start, goal, heuristic=manhattan):
	"""Return the shortest path from start to goal as a list of (row, col),
	or None if no path exists."""
	tie = count()
	open_heap = [(heuristic(start, goal), next(tie), start)]
	came_from = {}
	g_score = {start: 0}
	closed = set()

	while open_heap:
		_, _, current = heapq.heappop(open_heap)
		if current == goal:
			return _reconstruct(came_from, current)
		if current in closed:
			continue
		closed.add(current)

		for nxt in neighbors(grid, current):
			tentative = g_score[current] + 1
			if tentative < g_score.get(nxt, float('inf')):
				came_from[nxt] = current
				g_score[nxt] = tentative
				f = tentative + heuristic(nxt, goal)
				heapq.heappush(open_heap, (f, next(tie), nxt))
	return None


def _reconstruct(came_from, node):
	path = [node]
	while node in came_from:
		node = came_from[node]
		path.append(node)
	path.reverse()
	return path


def find(grid, ch):
	for r, row in enumerate(grid):
		c = row.find(ch)
		if c != -1:
			return (r, c)
	raise ValueError("grid has no '%s' cell" % ch)


def render(grid, path):
	cells = [list(row) for row in grid]
	for r, c in path:
		if cells[r][c] == '.':
			cells[r][c] = '*'
	return '\n'.join(''.join(row) for row in cells)


def main():
	grid = [
		"S....#....",
		".###.#.##.",
		".#...#..#.",
		".#.###..#.",
		".#.....##.",
		".####.#...",
		"......#.#G",
	]
	start, goal = find(grid, 'S'), find(grid, 'G')
	path = astar(grid, start, goal)
	if path is None:
		print("No path found")
		return
	print("Path length: %d" % (len(path) - 1))
	print(render(grid, path))


if __name__ == '__main__':
	main()
