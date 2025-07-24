import networkx as nx
import matplotlib.pyplot as plt
import re

def create_connection_graph(text_list):
    """
    Creates a connection graph from a list of texts.

    Args:
        text_list (list): A list of strings.

    Returns:
        networkx.Graph: A graph where nodes are names and edges represent
                        that the names appeared in the same text.
    """
    G = nx.Graph()
    for text in text_list:
        names = extract_names(text)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                G.add_edge(names[i], names[j])
    return G

def extract_names(text):
    """
    Extracts names from a string.

    Args:
        text (str): The string to extract names from.

    Returns:
        list: A list of names.
    """
    # This is a simple name extraction using regex.
    # A more advanced implementation would use NLP techniques.
    return re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)

def draw_graph(G):
    """
    Draws a graph using matplotlib.

    Args:
        G (networkx.Graph): The graph to draw.
    """
    nx.draw(G, with_labels=True)
    plt.show()
