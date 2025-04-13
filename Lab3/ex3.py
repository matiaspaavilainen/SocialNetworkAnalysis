import random
import time
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
import networkx.algorithms.community as nxcom
import numpy as np


def comm_quality(G, community, name):
    print(
        f"{name} community part of graph: {nxcom.community_utils.is_partition(G, community)}"
    )

    print(f"{name} modularity: {nxcom.modularity(G, community)}")

    print(f"{name} partition quality: {nxcom.partition_quality(G, community)}")


def exec_time(G, function, name):
    start = time.time_ns()
    comms = function(G)
    print(f"Time taken for {name}: {(time.time_ns() - start)} ns")


def all_for_graph(G, filename, positions):
    communities = girvan_newman(G)

    node_groups = []
    for com in next(communities):
        node_groups.append(list(com))

    print(f"Grivan: {node_groups}")

    com_for_eval = girvan_newman(G)
    comm_quality(G, next(com_for_eval), "Girvan")

    color_map = []
    edge_cmap = []
    for node in G:
        if node in node_groups[0]:
            color_map.append("blue")
        elif node in node_groups[1]:
            color_map.append("green")
        else:
            color_map.append("yellow")

    for edge in G.edges:
        if (edge[0] in node_groups[0] and edge[1] not in node_groups[0]) or (
            edge[0] not in node_groups[0] and edge[1] in node_groups[0]
        ):
            edge_cmap.append("red")
        else:
            edge_cmap.append("black")

    nx.draw(
        G, node_color=color_map, with_labels=True, edge_color=edge_cmap, pos=positions
    )
    plt.savefig(filename)
    plt.close()

    communities_kern = nx.algorithms.community.kernighan_lin_bisection(G)
    comm_quality(G, communities_kern, "Kern")
    print(f"Kern: {communities_kern}")

    communities_louv = nx.algorithms.community.louvain_communities(G)
    comm_quality(G, communities_louv, "Louv")
    print(f"Louv: {communities_louv}")

    communities_label = (
        nx.algorithms.community.label_propagation.label_propagation_communities(G)
    )
    comm_quality(G, communities_label, "Label")
    print(f"Label: {list(communities_label)}")

    exec_time(G, girvan_newman, "Girvan")
    exec_time(G, nxcom.kernighan_lin_bisection, "Kern")
    exec_time(G, nxcom.louvain_communities, "Louv")
    exec_time(G, nxcom.label_propagation.label_propagation_communities, "Label")


def main():
    G: nx.Graph = nx.karate_club_graph()
    pos_karate = nx.spring_layout(G)
    all_for_graph(G, filename="karateonlypng", positions=pos_karate)

    pathlen = nx.algorithms.average_shortest_path_length(G)
    print(f"Average path length: {pathlen}")

    # new graph
    all_x = [p[0] for p in pos_karate.values()]
    all_y = [p[1] for p in pos_karate.values()]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    pos_geometric = {}

    for i in range(20):
        x = random.uniform(
            min_x, max_x
        )  # Use uniform instead of randint for better distribution
        y = random.uniform(min_y, max_y)
        pos_geometric[i] = np.array([x, y])

    # Pass the positions to the random_geometric_graph function
    H: nx.Graph = nx.random_geometric_graph(20, pathlen, pos=pos_geometric)
    H = nx.relabel_nodes(H, {i: i + 34 for i in range(20)})

    # Update positions after relabeling
    pos_geometric_relabeled = {i + 34: pos for i, pos in pos_geometric.items()}

    # Combine graphs
    G = nx.union(G, H)

    # Combine positions
    combined_pos = {**pos_karate, **pos_geometric_relabeled}

    all_for_graph(G, filename="Extar20.png", positions=combined_pos)


if __name__ == "__main__":
    main()
