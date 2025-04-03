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


def main():
    pass


if __name__ == "__main__":
    main()
