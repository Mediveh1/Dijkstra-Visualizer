
import customtkinter as ctk
from tkinter import *
import matplotlib.pyplot as pp
import networkx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Dijkstra
import GraphClass


from tkinter import messagebox
window = ctk.CTk()
window.title(" Dijkstra Visualizer")

# Sub frame
sub_frame = ctk.CTkFrame(window,fg_color="transparent")
sub_frame.grid(sticky="nsew")
sub_frame.columnconfigure(1, weight=1)
sub_frame.rowconfigure(0, weight=1)

# sub_frame_1 containing all the widgets
sub_frame_1 = ctk.CTkFrame(sub_frame)
sub_frame_1.grid(row=0, column=0, ipadx=30)

# sub_frame_2 containing the plotted graph
sub_frame_2 = ctk.CTkFrame(sub_frame, width=1)
sub_frame_2.grid(row=0, column=1,  padx=20)


# Input frame 1
frame1 = ctk.CTkFrame(sub_frame_1,fg_color="transparent")
frame1.grid(pady=20,sticky="n")
frame1.columnconfigure(1, weight=1)
frame1.rowconfigure(5, weight=1)

# Input frame 2
frame2 = ctk.CTkScrollableFrame(sub_frame_1, width=250, height=100)
frame2.grid(sticky="n")
frame2.columnconfigure(2, weight=1)
frame2.rowconfigure(1, weight=1)


# plot frame
frame3 = ctk.CTkFrame(sub_frame_1)
frame3.grid(sticky="n", pady=20)
frame3.columnconfigure(1,weight=1)
frame3.rowconfigure(2,weight=1)
frame3.configure(fg_color="transparent")

# Variables
nodes = StringVar()
edges = StringVar()
source_Val = StringVar()
destination_Val = StringVar()
entry_var = StringVar()

############################################################



class node:
    def __init__(self, from_val, to_val, weight):
        self.from_val = from_val
        self.to_val = to_val
        self.weight = weight


edgeList = []


def list_entry(n, *args):
    r = 0
    try:
        if n.isnumeric():
            n = int(n)
            for child in frame2.winfo_children():
                child.destroy()
            edgeList.clear()
            for i in range(n):
                from_label = ctk.CTkLabel(frame2, text="From")
                from_label.grid(row=r, column=0, padx=5)
                from_val = ctk.CTkEntry(frame2, width=30)
                from_val.grid(row=r + 1, column=0, padx=5)
                to_label = ctk.CTkLabel(frame2, text="to")
                to_label.grid(row=r, column=1, padx=5)
                to_value = ctk.CTkEntry(frame2, width=30)
                to_value.grid(row=r + 1, column=1, padx=5)
                weight = ctk.CTkLabel(frame2, text="Weight")
                weight.grid(row=r, column=2, padx=5)
                weight_value = ctk.CTkEntry(frame2, width=30)
                weight_value.grid(row=r + 1, column=2, padx=5)
                r = r + 2
                edgeList.append(node(from_val, to_value, weight_value))
    except:
        print("error encountered invalid value for number of edges")


def enter():
    n = nodes.get()
    n = int(n)
    graph = GraphClass.Graph()
    for i in range(len(edgeList)):
        from_val = int(edgeList[i].from_val.get())
        to_val = int(edgeList[i].to_val.get())
        weight = int(edgeList[i].weight.get())
        graph.add_vertex(vertex=from_val)
        graph.add_vertex(vertex=to_val)
        if graph_type.get() == "Undirected":
            graph.add_edge_undirected(vertex1=from_val, vertex2=to_val, weight=weight)
        else:
            graph.add_edge_directed(vertex1=from_val, vertex2=to_val, weight=weight)
    dijkstra = Dijkstra.DijkstraSolver(number_of_nodes=int(n), graph=graph, graphType=graph_type.get())
    result_graph = dijkstra.solve(source=int(source_Val.get()),destination_Val=int(destination_Val.get()))
    pos = networkx.spring_layout(result_graph)
    networkx.draw(result_graph, pos, with_labels=True, font_weight='bold')
    labels = networkx.get_edge_attributes(result_graph, 'weight')
    networkx.draw_networkx_edge_labels(result_graph, pos, edge_labels=labels)
    pp.show()
    graph_inside_tkinter(result_graph)



def graph_inside_tkinter(graph):
    for widget in sub_frame_2.winfo_children():
        widget.destroy()
    # Create a canvas to embed the graph
    canvas = ctk.CTkCanvas(sub_frame_2, width=600, height=400)
    canvas.grid()

    # Convert the NetworkX graph to a matplotlib figure
    pos = networkx.spring_layout(graph)  # You can use a different layout algorithm
    fig, ax = pp.subplots()

    # Draw nodes
    networkx.draw_networkx_nodes(graph, pos, ax=ax, node_size=500, node_color='skyblue', node_shape="o")

    # Draw edges with weights
    edge_labels = networkx.get_edge_attributes(graph, 'weight')
    edges = networkx.draw_networkx_edges(graph, pos, ax=ax, width=1.0, arrowsize=20, arrowstyle="simple")

    # Draw edge labels
    networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    # Draw node labels
    networkx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color='black')

    # Embed the matplotlib figure in the Tkinter canvas
    canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().grid()



#############################################################################

# tracing on changes
entry_var.trace_add("write", lambda *args: list_entry(Number_of_edges.get(), *args))


# title
title = ctk.CTkLabel(frame1, text="Dijkstra Visualizer", text_color="black", font=("Poplar Std", 30), pady=35, padx=35)
title.grid(row=0, column=0)

# widget for number of nodes
Number_of_Nodes_label = ctk.CTkLabel(frame1, text="Number of Nodes")
Number_of_Nodes_label.grid(row=1, column=0)
Enter_Nodes_Entry = ctk.CTkEntry(frame1, textvariable=nodes)
Enter_Nodes_Entry.grid(row=2, column=0, padx=10)

# widget for number of edges
Number_of_Edges_label = ctk.CTkLabel(frame1, text="Number of Edges")
Number_of_Edges_label.grid(row=1, column=1)
Number_of_edges = ctk.CTkEntry(frame1, textvariable=entry_var)
Number_of_edges.grid(row=2, column=1, padx=5)

# widget for graph type
graph_type_values = ["Directed", "Undirected"]
graph_type = ctk.CTkComboBox(frame1, values=graph_type_values)
graph_type.grid(row=5, column=1, pady=15)
graph_type_label = ctk.CTkLabel(frame1, text="Select Graph Type: ")
graph_type_label.grid(row=5, column=0, padx=5, pady=15)

# source destination
source = ctk.CTkLabel(frame1, text="source")
source.grid(row=3,column=0)
source_value = ctk.CTkEntry(frame1, textvariable=source_Val)
source_value.grid(row=4, column=0)
destination = ctk.CTkLabel(frame1, text="destination")
destination.grid(row=3,column=1)
destination_value = ctk.CTkEntry(frame1, textvariable= destination_Val)
destination_value.grid(row=4, column=1)

# widget for plotting
plot = ctk.CTkLabel(frame3, text="Plot Shortest Path")
plot.grid(pady=10)
plot_button = ctk.CTkButton(frame3, command=enter,  text="PLOT GRAPH")
plot_button.grid(pady=10)


window.mainloop()
