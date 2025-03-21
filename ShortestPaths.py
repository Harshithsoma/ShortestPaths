class GridPathFinder:
    def __init__(self, grid, terminals):
        self.grid = grid
        self.terminals = terminals
        self.bounding_boxes = self.computeBoundingBoxes()
        self.reduced_grid = self.removeIrrelevantVertices()

    def computeBoundingBoxes(self):
        bounding_boxes = {}
        for (si, ti) in self.terminals:
            min_x, max_x = min(si[0], ti[0]), max(si[0], ti[0])
            min_y, max_y = min(si[1], ti[1]), max(si[1], ti[1])
            bounding_boxes[(si, ti)] = ((min_x, max_x), (min_y, max_y))
        return bounding_boxes

    def removeIrrelevantVertices(self):
        reduced_grid = set()
        for (si, ti), ((min_x, max_x), (min_y, max_y)) in self.bounding_boxes.items():
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    reduced_grid.add((x, y))
        return reduced_grid

    def computeShortestPath(self, start, end):
        from collections import deque
        queue = deque([(start, [start])])
        visited = set([start])
        while queue:
            current, path = queue.popleft()
            if current == end:
                return path
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if neighbor in self.reduced_grid and neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return None  # No path found

    def reroutePath(self, start, end, existing_paths):
        # Apply heuristic rerouting to resolve conflicts
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_start = (start[0] + dx, start[1] + dy)
            new_end = (end[0] + dx, end[1] + dy)
            if new_start in self.reduced_grid and new_end in self.reduced_grid:
                new_path = self.computeShortestPath(new_start, new_end)
                if new_path and not any(set(new_path) & set(p) for p in existing_paths):
                    return new_path
        return None

    def findDisjointPaths(self):
        paths = []
        for (si, ti) in self.terminals:
            path = self.computeShortestPath(si, ti)
            if any(set(path) & set(p) for p in paths):
                path = self.reroutePath(si, ti, paths)
            if not path:
                return None  # No solution found
            paths.append(path)
        return paths
