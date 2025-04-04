import os
import random
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(
    data_list,
    title="Histogram",
    xlabel="Value",
    file=None,
):
    ylabel = "Frequency"
    plt.figure(figsize=(10, 6), clear=True)

    plt.hist(data_list)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    plt.savefig(file)
    plt.close()


def load_facebook_ego_network(ego_id):
    base_path = "facebook"  # Folder where the data is stored

    # Load edges (space-delimited)
    edges_file = os.path.join(base_path, f"{ego_id}.edges")
    G: nx.Graph = nx.read_edgelist(edges_file, delimiter=" ", nodetype=int)

    # Add the ego node (may not be in edge list)
    G.add_node(int(ego_id))
    return G


def main():
    ego_id = 0
    G = load_facebook_ego_network(ego_id)
    G1 = load_facebook_ego_network(107)
    G2 = load_facebook_ego_network(348)
    G3 = load_facebook_ego_network(414)
    G4 = load_facebook_ego_network(686)
    G5 = load_facebook_ego_network(1684)
    G6 = load_facebook_ego_network(1912)
    G7 = load_facebook_ego_network(3437)
    G8 = load_facebook_ego_network(3980)

    G = nx.disjoint_union_all([G, G1, G2, G3, G4, G5, G6, G7, G8])

    print(
        f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
    )

    # Visualize the graph with circles highlighted
    plt.figure(figsize=(12, 12))

    # Use a layout that works well for community structure
    pos = nx.spring_layout(G, seed=42)

    # Draw all nodes and edges
    nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_nodes(G, pos)

    plt.axis("off")
    plt.savefig(f"facebook_ego_{ego_id}.png", dpi=300)
    plt.close()

    # betweennes
    between = list(nx.betweenness_centrality(G, k=1).values())
    plot_histogram(
        between,
        "Betweennes centrality",
        xlabel="Betweennes",
        file="between_centr_2.png",
    )

    # closeness
    closness = list(nx.closeness_centrality(G).values())
    plot_histogram(
        closness,
        "Closeness cetnrality",
        xlabel="Closeness",
        file="closeness_2.png",
    )

    # degree centraliy
    degree_centr = list(nx.degree_centrality(G).values())
    plot_histogram(
        degree_centr,
        "Degree centrality",
        xlabel="Degree CEntarality",
        file="degree_centrality_2.png",
    )

    clustering = nx.clustering(G).values()

    plt.plot(clustering, marker=".", linestyle="")

    plt.title("clustering")
    plt.tight_layout()

    plt.savefig("clusterign2.png")
    plt.close()

    plot_histogram(
        clustering,
        title="Clustering",
        xlabel="Coefficient",
        file="clustering_hist_2.png",
    )


if __name__ == "__main__":
    main()
