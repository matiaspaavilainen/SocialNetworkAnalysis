import networkx as nx
import matplotlib.pyplot as plt
import pickle


def main():
    with open("karate_club_coords.pkl", "rb") as file:
        data = pickle.load(file, encoding="bytes")
        print(data.keys())
    G = nx.Graph(data)
    # print(nx.adjacency_matrix(G))
    nx.draw(G, with_labels=True)
    plt.savefig("karate.png")


if __name__ == "__main__":
    main()
