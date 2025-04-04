import os
import networkx as nx
import matplotlib.pyplot as plt


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
    base_path = "facebook"

    edges_file = os.path.join(base_path, f"{ego_id}.edges")
    G: nx.DiGraph = nx.read_edgelist(
        edges_file, delimiter=" ", nodetype=int, create_using=nx.DiGraph()
    )

    G.add_node(int(ego_id))
    return G


def main():
    ids = [0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980]
    G = nx.DiGraph()
    for id in ids:
        H = load_facebook_ego_network(id)
        G = nx.disjoint_union(G, H)

    # get 100 nodes
    print("Finding nodes")
    # indeg centrality or degree
    indeg = G.in_degree()
    nodes = []
    value_list = list(dict(indeg).values())
    print(max(value_list))
    i = 0
    while len(nodes) < 100:
        if value_list[i] >= 2 and value_list[i] <= 10:
            nodes.append(list(dict(indeg).keys())[i])
        i = i + 1

    G = G.subgraph(nodes).copy()
    print(G)

    G = G.to_undirected()

    plt.figure(figsize=(12, 12))

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_nodes(G, pos)

    plt.axis("off")
    plt.savefig(f"facebook.png", dpi=300)
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
