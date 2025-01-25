#Name: Lopez, James Ryan
#Year & Section: 2A
#Date: 12/15/2024

import math

def greedy_best_first_search(start, goal, nodes, canvas, adjacency_matrix):
    open_list = [(heuristic(start, goal, nodes), start)]
    came_from = {}
    visited = set()

    while open_list:
        open_list.sort(key=lambda x: x[0])
        *_, current = open_list.pop(0)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            for i in range(len(path) - 1):
                start_node = nodes[path[i]]
                end_node = nodes[path[i + 1]]
                canvas.create_line(start_node[0], start_node[1], end_node[0], end_node[1],
                                   fill="violet", width=3, tags="path")
                canvas.update()
                canvas.after(500)
            return path

        for neighbor in range(len(nodes)):
            if neighbor not in visited and adjacency_matrix[current][neighbor] != float('inf'):
                open_list.append((heuristic(neighbor, goal, nodes), neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current

                current_x, current_y, *_  = nodes[current]
                neighbor_x, neighbor_y, *_  = nodes[neighbor]
                canvas.create_line(current_x, current_y, neighbor_x, neighbor_y, fill="white", width=2)
                canvas.update()
                canvas.after(1000)

        canvas.delete("processing_edge")

    print("No path found")
    return None

def heuristic(node, goal, nodes):
    node_x, node_y, *_ = nodes[node]
    goal_x, goal_y, *_ = nodes[goal]
    return math.sqrt((node_x - goal_x) ** 2 + (node_y - goal_y) ** 2)