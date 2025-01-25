#Name: Lopez, James Ryan
#Year & Section: 2A
#Date: 12/15/2024

import heapq
import math

def a_star(start, goal, max_nodes, adjacency_matrix, nodes, canvas):
    open_set = [(0, start)]
    g_costs = {i: float('inf') for i in range(max_nodes)}
    g_costs[start] = 0
    previous_nodes = {i: None for i in range(max_nodes)}
    f_costs = {i: float('inf') for i in range(max_nodes)}
    f_costs[start] = heuristic(start, goal, nodes)
    open_set_entries = {start}

    while open_set:
        *_, current = heapq.heappop(open_set)
        open_set_entries.remove(current)

        if current == goal:
            break

        for neighbor in range(max_nodes):
            if adjacency_matrix[current][neighbor] != float('inf'):
                tentative_g_cost = g_costs[current] + adjacency_matrix[current][neighbor]

                if tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_costs[neighbor] = g_costs[neighbor] + heuristic(neighbor, goal, nodes)
                    previous_nodes[neighbor] = current

                    if neighbor not in open_set_entries:
                        heapq.heappush(open_set, (f_costs[neighbor], neighbor))
                        open_set_entries.add(neighbor)

                    current_x, current_y, *_ = nodes[current]
                    neighbor_x, neighbor_y, *_ = nodes[neighbor]
                    canvas.create_line(current_x, current_y, neighbor_x, neighbor_y, fill="white", width=3)
                    canvas.update()
                    canvas.after(1000)

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    for i in range(len(path) - 1):
        start_node = nodes[path[i]]
        end_node = nodes[path[i + 1]]
        canvas.create_line(start_node[0], start_node[1], end_node[0], end_node[1], fill="violet", width=4, tags="path")
        canvas.update()
        canvas.after(500)

    return path

def heuristic(node, goal, nodes):
    node_x, node_y, *_ = nodes[node]
    goal_x, goal_y, *_ = nodes[goal]
    return math.sqrt((node_x - goal_x) ** 2 + (node_y - goal_y) ** 2)