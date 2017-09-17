# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 21:26:14 2017

@author: suzie
"""

import networkx as nx
import matplotlib.pyplot as plt

def mapPath(start, end, nodes = ["hall1", "hall2", "100", "101", "102"],
        edges = [("hall1", "100", {'weight':1}), 
             ("hall1", "101", {'weight':2}),
             ("100", "101", {'weight':1}),
             ("hall1", "hall2", {'weight':3}),
             ("hall2", "102", {'weight':1})]):
    G=nx.Graph()
    
    G.add_nodes_from(nodes)
    edges = 
    G.add_edges_from(edges)
    
    print(nx.shortest_path(G, start, end))
    print(nx.shortest_path_length(G, start, end))
    #print(G.nodes())
    #print(G.edges())

    nx.draw(G)
    plt.show()

    return (nx.shortest_path(G, start, end),
           nx.shortest_path_length(G, start, end))
