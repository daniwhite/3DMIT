# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 21:26:14 2017

@author: suzie
"""

import networkx as nx
import matplotlib.pyplot as plt

def mapPath(start, end, nodes = ["hall1", "hall2", "hall3", "hall4", "hall5", "hall6", "100", "101", "102", "103", "104", "105", "106", "107", "301", "302", "303", "401", "402"],
        edges = [("hall1", "100", {'weight':1}), 
             ("hall1", "101", {'weight':2}),
             ("hall5", "103", {'weight':1}),
             ("hall5", "104", {'weight':2}),
             ("hall6", "105", {'weight':3}),
             ("hall1", "102", {'weight':1}),
             ("hall6", "106", {'weight':2}),
             ("hall1", "hall2", {'weight':7}),
             ("hall2", "hall3", {'weight':10}),
             ("hall3", "301", {'weight':2}),
             ("hall3", "302", {'weight':3}),
             ("hall3", "303", {'weight':2}),
             ("hall3", "hall4", {'weight':10}),
             ("hall4", "hall5", {'weight':9}),
             ("hall5", "hall6", {'weight':12}),
             ("hall4", "401", {'weight':1}),
             ("hall4", "402", {'weight':2}),
             ("hall6", "107", {'weight':3})]):
    
    G=nx.Graph()
    
    G.add_nodes_from(nodes)
    #edges = 
    G.add_edges_from(edges)
    
    print(nx.shortest_path(G, start, end))
    print(nx.shortest_path_length(G, start, end))
    #print(G.nodes())
    #print(G.edges())

    nx.draw(G)
    plt.show()

    return (nx.shortest_path(G, start, end),
           nx.shortest_path_length(G, start, end))

print(mapPath("101", "107"))