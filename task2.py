import networkx as nx
import matplotlib.pyplot as plt
import pickle


def main():
    with open("karate_club_coords.pkl", "rb") as file:
        data = pickle.load(file, encoding="bytes")

    G = nx.karate_club_graph()

    mapping = {}
    for i in G.nodes():
        mapping[i] = i + 1

    G = nx.relabel_nodes(G, mapping)

    pos = {}
    for club in data:
        pos[int(club)] = data[club]

    # Graph
    plt.figure(figsize=(10, 8))
    plt.title("Karate network")
    nx.draw(G, pos=pos, with_labels=True)
    plt.savefig("karate.png")

    # Adjacency matrix
    adj_matrix = nx.adjacency_matrix(G).toarray()
    plt.figure(clear=True)
    plt.matshow(adj_matrix)
    plt.savefig("adjacency_matrix.png")

    # Centrality
    degree_centrality_values = []
    for node in G:
        centrality = nx.degree_centrality(G)
        degree_centrality_values.append(centrality[node])

    plt.figure(clear=True)
    plt.xlabel("Nodes")
    plt.ylabel("Centrality")
    plt.plot(G.nodes(), degree_centrality_values)
    plt.savefig("karate_centrality.png")

    # Largest and smallest
    S = max([G.subgraph(c).copy() for c in nx.connected_components(G)])
    M = min([G.subgraph(c).copy() for c in nx.connected_components(G)])

    plt.figure(clear=True)
    nx.draw(S, pos=pos, with_labels=True)
    plt.savefig("largest_cc.png")

    print(f"Whole: {nx.diameter(G)}, Largest: {nx.diameter(S)}")


if __name__ == "__main__":
    main()
