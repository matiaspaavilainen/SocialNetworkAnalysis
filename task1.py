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


def stats(G, filename):
    # page rank
    page_ranks = list(nx.pagerank(G).values())
    plot_histogram(
        page_ranks,
        "Page Ranks",
        xlabel="Rank",
        file=f"page_rank_{filename}.png",
    )

    # degree centraliy
    degree_centr = list(nx.degree_centrality(G).values())
    plot_histogram(
        degree_centr,
        "Degree centrality",
        xlabel="Degree CEntarality",
        file=f"degree_centrality_{filename}.png",
    )

    # eigen centr
    eigen_centr = list(nx.eigenvector_centrality(G).values())
    plot_histogram(
        eigen_centr,
        "Eigen Centrality",
        xlabel="Eigen",
        file=f"eigen_centrality_{filename}.png",
    )

    # betweennes
    between = list(nx.betweenness_centrality(G, k=1).values())
    plot_histogram(
        between,
        "Betweennes centrality",
        xlabel="Betweennes",
        file=f"between_centr_{filename}.png",
    )

    # closeness
    closness = list(nx.closeness_centrality(G).values())
    plot_histogram(
        closness,
        "Closeness cetnrality",
        xlabel="Closeness",
        file=f"closeness_{filename}.png",
    )

    clustering = nx.clustering(G).values()

    plt.plot(clustering, marker=".", linestyle="")

    plt.title(f"clustering_{filename}")
    plt.tight_layout()

    plt.savefig(f"clusterign_{filename}.png")
    plt.close()

    plot_histogram(
        clustering, title="Clustering", xlabel="Coefficient", file="clustering_hist.png"
    )

    # global clustering idk
    global_clust = nx.average_clustering(G)
    print(f"Total clustering: {global_clust}")


def main():
    edges_df = pd.read_csv("edges.csv")
    G: nx.DiGraph = nx.from_pandas_edgelist(
        edges_df,
        source="id_1",
        target="id_2",
        create_using=nx.DiGraph(),
    )

    features_df = pd.read_csv("features.csv")
    targets_df = pd.read_csv("target.csv")

    for node_id, data in features_df.iterrows():
        if node_id in G:
            G.nodes[node_id]["features"] = ",".join(map(str, data.values))

    for node_id, target in targets_df.iterrows():
        if node_id in G:
            G.nodes[node_id]["target"] = int(target.values[0])

    # get 100 nodes with highest in deg centr
    sorted100 = dict(
        sorted(
            nx.in_degree_centrality(G).items(),
            key=lambda item: item[1],
            reverse=True,
        )[0:100]
    )
    top100_nodes = list(sorted100.keys())
    G = G.subgraph(top100_nodes).copy()

    G = G.to_undirected()

    # degree
    degrees = dict(G.degree())
    highest_degree_node = max(degrees, key=degrees.get)
    print(f"Node, degree: {highest_degree_node}, {degrees[highest_degree_node]}")

    # Write to GEXF
    nx.write_gexf(G, "network.gexf")
    # get componetns
    components = list(nx.connected_components(G))

    print(f"Connected components: {len(components)}")

    components.sort(key=len, reverse=True)
    for comp in components:
        print(f"Number of nodes: {len(comp)}")

    stats(G, "whole")
    stats(G.subgraph(max(nx.connected_components(G), key=len)).copy(), "largest")

    # subgraph
    bipart = None
    while not bipart:
        sample_nodes = random.sample(list(G.nodes()), min(32, len(G.nodes())))
        sample_graph: nx.Graph = G.subgraph(sample_nodes).copy()
        if nx.is_bipartite(sample_graph) and sample_graph.number_of_edges() > 2:
            bipart = sample_graph

    print(f"Bipartite: {bipart}")


if __name__ == "__main__":
    main()
