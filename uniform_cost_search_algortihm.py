#Name: Lopez, James Ryan
#Year & Section: 2A
#Date: 12/15/2024

import heapq

def uniform_cost_search(start, goal, nodes, adjacency_matrix, canvas):
    open_list = []
    closed_list = set()
    came_from = {}
    cost_so_far = {}

    heapq.heappush(open_list, (0, start))
    cost_so_far[start] = 0
    came_from[start] = None

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()

            for i in range(len(path) - 1):
                start_node = nodes[path[i]]
                end_node = nodes[path[i + 1]]
                canvas.create_line(start_node[0], start_node[1], end_node[0], end_node[1], fill="violet", width=3, tags="path")
                canvas.update()
                canvas.after(500)

            return path

        closed_list.add(current_node)

        for neighbor in range(len(nodes)):
            if adjacency_matrix[current_node][neighbor] != float('inf') and neighbor not in closed_list:
                new_cost = current_cost + adjacency_matrix[current_node][neighbor]
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor))
                    came_from[neighbor] = current_node

                    neighbor_x, neighbor_y, *_ = nodes[neighbor]
                    current_x, current_y, *_  = nodes[current_node]
                    canvas.create_line(current_x, current_y, neighbor_x, neighbor_y, fill="white", width=2)
                    canvas.update()
                    canvas.after(1000)

    return None