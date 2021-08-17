# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:29:14 2021

@author: Jackie
"""

import pydot
import networkx as nx
import pandas as pd
import numpy as np

#Transition probabilities
#df_Q = pd.read_csv('data/Q_matrix.csv', index_col=0)
path_tran = r"C:\Users\Jackie.MEDICINE\Desktop\VAME-master\avrg_20.npy"
df_Q_temp  = np.load(path_tran)


df_Q = pd. DataFrame(df_Q_temp)
df_Q[df_Q < 0.1] = 0
df_Q = df_Q.round(2)


#Possible states
int_states = list(range(0,20))
str_state = list(map(str, int_states))
states = str_state

# create a function that maps transition probability dataframe
# to markov edges and weights

def _get_markov_edges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] = Q.loc[idx,col]
    return edges

edges_wts = _get_markov_edges(df_Q)
#pprint(edges_wts)

# create graph object
G = nx.MultiDiGraph()

# nodes correspond to states
G.add_nodes_from(states)
print(f'Nodes:\n{G.nodes()}\n')

# edges represent transition probabilities
for k, v in edges_wts.items():

    if v > 0.0:
        tmp_origin, tmp_destination = k[0], k[1]
        G.add_edge(tmp_origin, tmp_destination, weight=v, label=v)

pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos)

# create edge labels for jupyter plot but is not necessary
edge_labels = {(n1,n2):d['label'] for n1,n2,d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
nx.drawing.nx_pydot.write_dot(G, 'markov.dot')

(graph,) = pydot.graph_from_dot_file('markov.dot')
graph.write_png('markov.png')