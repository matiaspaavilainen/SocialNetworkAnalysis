import statistics
import networkx as nx
import matplotlib.pyplot as plt
from random import choice, randint

import numpy as np


def genereate_graph():
    G = nx.Graph()
    names = ["John", "Jane", "Lux", "Bard"]
    for i in range(1, 51):
        label = choice(names)
        G.add_node(i, label=label)
        # random amount of edges
        for j in range(0, randint(1, 5)):
            rand = randint(1, i)
            if rand == i:
                G.add_edge(i, rand + 1)
            else:
                G.add_edge(i, rand)

    return G


def remove_rand(graph):
    avg_degrees = []
    avg_degree_c = []
    while len(list(graph)) > 1:
        rand = choice(list(graph.nodes()))
        graph.remove_node(rand)
        _, _, centrality, avg_degree = degrees(graph)
        avg_degrees.append(avg_degree)
        avg_degree_c.append(max(centrality))

    print("Avg degrees: ", avg_degrees)
    nodes = list(range(len(avg_degree_c), 0, -1))

    fig = plt.figure("Degrees After", figsize=(12, 6))
    axgrid = fig.add_gridspec(4, 2)
    ax1 = fig.add_subplot(axgrid[:, :1])
    ax1.bar(nodes, avg_degree_c)
    ax1.xaxis.set_inverted(True)
    ax1.set_title("Max Degree Centrality at # of nodes")
    ax1.set_ylabel("Degree Centrality")
    ax1.set_xlabel("Nodes")
    ax2 = fig.add_subplot(axgrid[:, 1:])
    ax2.xaxis.set_inverted(True)
    ax2.bar(nodes, avg_degrees)
    ax2.set_title("Avg degrees at # of nodes")
    ax2.set_ylabel("Degrees")
    ax2.set_xlabel("# of Nodes")
    plt.savefig("reg_rem.png")


def degrees(graph):
    degrees = nx.degree(graph)
    degs = []
    nodes = []
    for i in degrees:
        nodes.append(i[0])
        degs.append(i[1])

    avg_degree = statistics.mean(degs)

    degree_centrality_values = []
    for node in graph:
        centrality = nx.degree_centrality(graph)
        degree_centrality_values.append(centrality[node])

    return nodes, degs, degree_centrality_values, avg_degree


def draw_degrees(nodes, degs, d, file="degrees.png"):
    fig = plt.figure("Degrees", figsize=(12, 6))
    axgrid = fig.add_gridspec(4, 2)
    ax1 = fig.add_subplot(axgrid[:, :1])
    ax1.bar(nodes, d)
    ax1.set_title("Degree Centrality per node")
    ax1.set_ylabel("Degree Centrality")
    ax1.set_xlabel("Node")
    ax2 = fig.add_subplot(axgrid[:, 1:])
    ax2.bar(nodes, degs)
    ax2.set_title("Degrees per node")
    ax2.set_ylabel("Degrees")
    ax2.set_xlabel("Node")
    plt.savefig(file)


def visualize_graph(graph, file="graph.png"):
    # https://networkx.org/documentation/latest/auto_examples/drawing/plot_degree.html#sphx-glr-auto-examples-drawing-plot-degree-py

    plt.figure(clear=True)  # Create a new figure and clear previous content
    degree_sequence = sorted((d for n, d in graph.degree()), reverse=True)

    fig = plt.figure("Degree of a random graph", figsize=(8, 8))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 4)

    ax0 = fig.add_subplot(axgrid[0:3, :])
    Gcc = graph.subgraph(
        sorted(nx.connected_components(graph), key=len, reverse=True)[0]
    )
    pos = nx.spring_layout(Gcc, seed=10396953)
    nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of G")
    ax0.set_axis_off()

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.savefig(file)
    plt.close()  # Close the figure to free memory


def main():
    G = genereate_graph()
    print(f"Edges: {G.number_of_edges()}, Nodes: {G.number_of_nodes()}")
    visualize_graph(G)
    nodes, degs, d, avg = degrees(G)
    draw_degrees(nodes, degs, d)
    remove_rand(G)


if __name__ == "__main__":
    main()
