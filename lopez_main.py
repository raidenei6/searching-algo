#Name: Lopez, James Ryan
#Year & Section: 2A
#Date: 12/15/2024

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import math
import a_star_algorithm as a_star
import uniform_cost_search_algortihm as usc
import greedy_best_first_search_algorithm as greedy

drawing_node_enabled = False
drawing_edges_enabled = False
selecting_for_node_enabled = False
selected_node_for_edges = None
node_count = 0
selected_nodes = []
nodes = []
max_nodes = 50

def main():
    root = tk.Tk()
    root.geometry("1330x600")
    root.config(bg="#F0F0F0")

    style = ttk.Style()
    style.configure('TButton', background='violet', foreground='white', borderwidth=10)

    map_img_path = "map_img.png"
    map_img = Image.open(map_img_path)
    map_img = map_img.resize((1000, 600))
    map_img_tk = ImageTk.PhotoImage(map_img)

    canvas = tk.Canvas(root, width=998, height=599, bg="#000000")
    canvas.pack(side=tk.RIGHT, padx=110, pady=10)
    canvas.create_image(0, 1, image=map_img_tk, anchor=tk.NW)

    def distance_between_nodes(x, y):
        x1, y1, *_ = nodes[x]
        x2, y2, *_ = nodes[y]
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    adjacency_matrix = [[float('inf')]*max_nodes for _ in range(max_nodes)]
    for i in range(max_nodes):
        adjacency_matrix[i][i] = 0

    def add_edge_to_matrix(x, y, weight):
        adjacency_matrix[x][y] = weight
        adjacency_matrix[y][x] = weight

    def draw_node(event):
        global drawing_node_enabled, node_count, nodes
        if drawing_node_enabled and node_count < max_nodes:
            x, y = event.x, event.y
            r = 8
            node_id = canvas.create_oval(x-r, y-r, x+r, y+r, fill='blue', outline='black', width=1)
            nodes.append((x, y, node_id))
            node_count += 1

    def toggle_drawing():
        global drawing_node_enabled
        drawing_node_enabled = not drawing_node_enabled
        canvas.bind('<Button-1>', draw_node)

    def draw_edges(event):
        global drawing_edges_enabled, nodes, selected_node_for_edges
        if event.num == 3 and drawing_edges_enabled and len(nodes) > 1:
            x, y = event.x, event.y
            for i, (node_x, node_y, node_id) in enumerate(nodes):
                r = 8
                if (node_x - x)**2 + (node_y - y)**2 <= r**2:
                    if selected_node_for_edges is not None:
                        start_x, start_y, *_ = nodes[selected_node_for_edges]
                        weight = distance_between_nodes(selected_node_for_edges, i)
                        canvas.create_line(start_x, start_y, node_x, node_y, fill='black', width=4)
                        add_edge_to_matrix(selected_node_for_edges, i, weight)
                        print(f'Connecting node {nodes[selected_node_for_edges]} to node {nodes[i]} with weigth {round(weight, 2)}')
                        selected_node_for_edges = None
                        break
                    else:
                        selected_node_for_edges = i
                        print(f'Selected node {nodes[i]} for connection')
                        break
            if selected_node_for_edges is not None and (x-nodes[selected_node_for_edges][0])**2 + (y-nodes[selected_node_for_edges][1])**2 > r**2:
                selected_node_for_edges = None
                print('Connection cancelled (clicked outside a node).....')
    
    def toggle_connecting():
        global drawing_edges_enabled
        drawing_edges_enabled = not drawing_edges_enabled
        canvas.bind('<Button-3>', draw_edges)

    def selecting_a_node(event):
        global selecting_for_node_enabled, selected_nodes, nodes
        if selecting_for_node_enabled and len(selected_nodes) < 2:
            x, y = event.x, event.y
            for i, (node_x, node_y, node_id) in enumerate(nodes):
                r = 10
                if (node_x - x)**2 + (node_y - y)**2 <= r**2:
                    if i not in selected_nodes:
                        selected_nodes.append(i)
                        if len(selected_nodes) == 1:
                            canvas.itemconfig(node_id, fill='green')
                        elif len(selected_nodes) == 2:
                            canvas.itemconfig(node_id, fill='red')
                        print(f'Selected node {i} at ({node_x}, {node_y})')

                    break
            if len(selected_nodes) == 2:
                print(f'Selected nodes: {selected_nodes}')
                selecting_for_node_enabled = False
                print('Selection completed.....')

    def toggle_selecting():
        global selecting_for_node_enabled, selected_nodes
        selecting_for_node_enabled = not selecting_for_node_enabled
        selected_nodes = []
        canvas.bind('<Button-1>', selecting_a_node)

    def search_a_path():
        global selected_nodes

        if len(selected_nodes) != 2:
            messagebox.showerror('Error', 'Please select two node first')
            return
        
        start = selected_nodes[0]
        goal = selected_nodes[1]

        canvas.delete('path')

        if options_for_algorithn.get() == "A*":
            path = a_star.a_star(start, goal, max_nodes, adjacency_matrix, nodes, canvas)
            path_cost = calculate_path_cost(path)
        elif options_for_algorithn.get() == "UCS":
            path = usc.uniform_cost_search(start, goal, nodes, adjacency_matrix, canvas)
            path_cost = calculate_path_cost(path)
        elif options_for_algorithn.get() == "Greedy":
            path = greedy.greedy_best_first_search(start, goal, nodes, canvas, adjacency_matrix)
            path_cost = calculate_path_cost(path)
        else:
            messagebox.showerror('Error', 'Please select an algorithm')
            return
        
        for i in range(len(path)-1):
            start_node = nodes[path[i]]
            end_node = nodes[path[i + 1]]
            canvas.create_line(start_node[0], start_node[1], end_node[0], end_node[1], fill='violet', width=4, tags='path')
            canvas.update()
        
        cal_path_cost.config(text=f'Cost: {path_cost}')
        
    def calculate_path_cost(path):
        total_cost = 0
        for i in range(len(path)-1):
            total_cost += adjacency_matrix[path[i]][path[i+1]]
        return round(total_cost, 2)

    frame_for_btn = tk.Frame(root, bg="#F0F0F0", borderwidth=2, relief="raised")
    frame_for_btn.pack(padx=5, pady=5, side="left", fill="y")

    draw_node_btn = ttk.Button(frame_for_btn, text="Draw Node", command=toggle_drawing)
    draw_node_btn.pack(padx=10, pady=10, side="top")

    draw_edge_btn = ttk.Button(frame_for_btn, text="Draw Edge", command=toggle_connecting)
    draw_edge_btn.pack(padx=10, pady=10, side="top")

    selection_btn = ttk.Button(frame_for_btn, text="Start/Goal", command=toggle_selecting)
    selection_btn.pack(padx=10, pady=10, side="top")

    options = [
        "A*",
        "UCS",
        "Greedy"
    ]

    options_for_algorithn = ttk.Combobox(frame_for_btn, state="readonly", values=options)
    options_for_algorithn.set(options[0])
    options_for_algorithn.pack(side="top", padx=10, pady=10)

    search_path_btn = ttk.Button(frame_for_btn, text="Search Path", command=search_a_path)
    search_path_btn.pack(padx=10, pady=10, side="top")

    cal_path_cost = ttk.Label(frame_for_btn, text="Cost: N/A", font=('Arial', 8), width=25)
    cal_path_cost.pack(side="top", padx=10,pady=10)



    root.mainloop()


if __name__ == '__main__':
    main()
