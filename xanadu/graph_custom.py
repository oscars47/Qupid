import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import strawberryfields as sf
from strawberryfields.ops import GraphEmbed, MeasureFock


def graph_custom(n_nodes=10, show_plot=False):
    '''
    Generates a random connected graph with n_nodes nodes.
    The graph is guaranteed to be connected.
    '''
    # Start with a connected tree graph (which is minimally connected)
    G = nx.generators.trees.random_tree(n_nodes)
    
    # Add more edges to make the graph more complex and still connected
    # Number of additional edges is a random number between 1 and n_nodes (inclusive)
    n_extra_edges = np.random.randint(1, n_nodes + 1)
    
    for _ in range(n_extra_edges):
        # Randomly select two different nodes
        u, v = np.random.choice(n_nodes, 2, replace=False)
        
        # Add an edge between these nodes, if it doesn't already exist
        if not G.has_edge(u, v):
            G.add_edge(u, v)

    if show_plot:
        nx.draw(G, with_labels=True)
        plt.show()
    
    return G

def gen_random_search(G, n_nodes=10):
    '''
    perform GBS random sampling on the graph G
    '''
    # Get the adjacency matrix of the graph
    A = nx.adjacency_matrix(G).todense()
    print('got adjacency matrix')

    # Define the Strawberry Fields program
    prog = sf.Program(n_nodes)

    with prog.context as q:
        # Embed the graph into the GBS device
        GraphEmbed(A) | q
        # Measure in the Fock basis
        MeasureFock() | q

    # Setup the backend
    eng = sf.Engine(backend="gaussian")
    # Run the simulation
    results = eng.run(prog, shots = 1000)
    # Print the measurement results
    print("Measured photon numbers per mode:", results.samples)
    # save samples
    np.save('samples.npy', results.samples)

if __name__ == '__main__':
    G = graph_custom(show_plot=True)
    gen_random_search(G)