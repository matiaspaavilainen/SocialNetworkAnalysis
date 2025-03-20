import networkx as nx
import matplotlib.pyplot as plt
import pickle


def main():
    with open("karate_club_coords.pkl", "rb") as file:
        data = pickle.load(file, encoding="bytes")
    G = nx.Graph(data)
    nx.draw(G, with_labels=True)
    plt.savefig("karate.png")
    print(data)


if __name__ == "__main__":
    main()
