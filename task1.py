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
    edges_df = pd.read_csv("edges.csv")
    G: nx.Graph = nx.from_pandas_edgelist(edges_df, source="id_1", target="id_2")

    features_df = pd.read_csv("features.csv")
    targets_df = pd.read_csv("target.csv")

    for node_id, data in features_df.iterrows():
        if node_id in G:
            G.nodes[node_id]["features"] = ",".join(map(str, data.values))

    for node_id, target in targets_df.iterrows():
        if node_id in G:
            G.nodes[node_id]["target"] = int(target.values[0])

    # Write to GEXF
    nx.write_gexf(G, "network.gexf")

    # degree
    degrees = dict(G.degree())
    highest_degree_node = max(degrees, key=degrees.get)
    print(f"Node, degree: {highest_degree_node}, {degrees[highest_degree_node]}")

    # get componetns
    components = list(nx.connected_components(G))

    print(f"Connected components: {len(components)}")

    # page rank
    page_ranks = list(nx.pagerank(G).values())
    plot_histogram(
        page_ranks,
        "Page Ranks",
        xlabel="Rank",
        file="page_rank.png",
    )

    # degree centraliy
    degree_centr = list(nx.degree_centrality(G).values())
    plot_histogram(
        degree_centr,
        "Degree centrality",
        xlabel="Degree CEntarality",
        file="degree_centrality.png",
    )

    # eigen centr
    eigen_centr = list(nx.eigenvector_centrality_numpy(G).values())
    plot_histogram(
        eigen_centr,
        "Eigen Centrality",
        xlabel="Eigen",
        file="eigen_centrality.png",
    )

    # betweennes
    between = list(nx.betweenness_centrality(G, k=1).values())
    plot_histogram(
        between,
        "Betweennes centrality",
        xlabel="Betweennes",
        file="between_centr.png",
    )

    # closeness
    closness = list(nx.closeness_centrality(G).values())
    plot_histogram(
        closness,
        "Closeness cetnrality",
        xlabel="Closeness",
        file="closeness.png",
    )

    clustering = nx.clustering(G).values()

    plt.plot(clustering, marker=".", linestyle="")

    plt.title("clustering")
    plt.tight_layout()

    plt.savefig("clusterign.png")
    plt.close()

    plot_histogram(
        clustering, title="Clustering", xlabel="Coefficient", file="clustering_hist.png"
    )

    # global clustering idk
    global_clust = nx.average_clustering(G)
    print(f"total clustering: {global_clust}")

    # subgraph
    bipart = None
    while not bipart:
        sample_nodes = random.sample(list(G.nodes()), min(32, len(G.nodes())))
        sample_graph: nx.Graph = G.subgraph(sample_nodes).copy()
        if nx.is_bipartite(sample_graph) and sample_graph.number_of_edges() > 2:
            bipart = sample_graph

    print(bipart)
    visualize_graph(bipart, "bipart.png")


if __name__ == "__main__":
    main()
