# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 21:26:14 2017

@author: suzie
"""

import networkx as nx
import matplotlib.pyplot as plt
import processfloorplans
import random


def mapPath(start, end, img):
    contours = processfloorplans.find_room_contours(img)
    nodes = processfloorplans.compute_vertices(contours)
    edges = processfloorplans.compute_edges(img)
    if start == 'random':
        start = random.choice(nodes)
    if end == 'random':
        end = random.choice(nodes)
    
    
    G=nx.Graph()
    
    G.add_nodes_from(nodes)
##    edges =
    G.add_edges_from(edges)
    
    print(nx.shortest_path(G, start, end))
    print(nx.shortest_path_length(G, start, end))
    #print(G.nodes())
    #print(G.edges())

    nx.draw(G)
    plt.show()

    return (nx.shortest_path(G, start, end),
           nx.shortest_path_length(G, start, end))

mapPath('random', 'random',
        '/Users/jennahimawan/Desktop/1_0.png')
