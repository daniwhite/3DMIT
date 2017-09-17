# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 21:26:14 2017

@author: suzie
"""

import networkx as nx
G=nx.Graph()

nodes = ["hall1", "hall2", "100", "101", "102"]
G.add_nodes_from(nodes)
edges = [("hall1", "100", {'weight':1}), 
         ("hall1", "101", {'weight':2}),
         ("100", "101", {'weight':1}),
         ("hall1", "hall2", {'weight':3}),
         ("hall2", "102", {'weight':1})]
G.add_edges_from(edges)


print(nx.shortest_path(G, "101", "102"))
#print(G.nodes())
#print(G.edges())