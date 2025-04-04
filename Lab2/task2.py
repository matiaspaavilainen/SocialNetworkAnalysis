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


def dist(G, centrality, name):
    # distance between centarlities

    highest = list(centrality.keys())[
        list(centrality.values()).index(max(list(centrality.values())))
    ]

    highest_val = centrality[highest]

    del centrality[highest]
    second = list(centrality.keys())[
        list(centrality.values()).index(max(list(centrality.values())))
    ]

    while centrality[second] == highest_val:
        del centrality[second]
        second = list(centrality.keys())[
            list(centrality.values()).index(max(list(centrality.values())))
        ]

    try:
        dist = nx.shortest_path_length(G, highest, second)
    except nx.exception.NetworkXNoPath:
        print(f"No path for {name}")
        return

    print(f"Shortest distance for {name}: {dist}")


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
    i = 0
    while len(nodes) < 100:
        if value_list[i] >= 2 and value_list[i] <= 10:
            nodes.append(list(dict(indeg).keys())[i])
        i = i + 1

    G = G.subgraph(nodes).copy()
    G: nx.Graph = G.to_undirected()

    nx.write_gexf(G, "facebook.gexf")

    # betweennes
    between = nx.betweenness_centrality(G)
    plot_histogram(
        list(between.values()),
        "Betweennes centrality",
        xlabel="Betweennes",
        file="between_centr_2.png",
    )

    # closeness
    closness = nx.closeness_centrality(G)
    plot_histogram(
        list(closness.values()),
        "Closeness cetnrality",
        xlabel="Closeness",
        file="closeness_2.png",
    )

    # degree centraliy
    degree_centr = nx.degree_centrality(G)
    plot_histogram(
        list(degree_centr.values()),
        "Degree centrality",
        xlabel="Degree CEntarality",
        file="degree_centrality_2.png",
    )

    dist(G, degree_centr, "Degree")
    dist(G, closness, "Closeness")
    dist(G, between, "Betweennes")

    # subgaph
    sorted16 = dict(
        sorted(
            degree_centr.items(),
            key=lambda item: item[1],
            reverse=True,
        )[0:16]
    )
    sub = nx.subgraph(G, sorted16)

    nx.write_gexf(sub, "facebook_sub.gexf")

    clustering = nx.clustering(G)

    plt.plot(list(clustering.values()), marker=".")

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

    dist(G, clustering, "clustering")

    degrees = [d for _, d in G.degree()]

    plot_histogram(degrees, file="Degree")


if __name__ == "__main__":
    main()
