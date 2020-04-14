#!/usr/bin/env python
# coding: utf-8

# In[1]:


# rankings.py - takes in 'data.csv' of results and returns a
# dictionary of PageRanks.

import pandas as pd
import networkx as nx
import operator
import csv

# build edgelist
data = pd.read_csv('ultimate_sets_clean.csv') # 6 column cleaned data
data2 = data[['winner_global_id', 'loser_global_id']] # data with only IDs
edgelist = []
for i in range(0, len(data2)):
    edgelist.append(str(data2['winner_global_id'][i]) + ' '
                   + str(data2['loser_global_id'][i]))

# construct digraph
g = nx.DiGraph()
for i, row in data2.iterrows():
    g.add_edge(str(row[1]), str(row[0]), attr_dict=row[2:].to_dict())
    
# compute dictionary of (id: pagerank)
pr = nx.pagerank(g)

# sort dictionary by PageRank
pageranks = dict(sorted(pr.items(), key=operator.itemgetter(1),reverse=True))

# write dictionary to pageranks.csv
f = csv.writer(open('pageranks.csv', 'w'))
f.writerow(['ID', 'PageRank'])
for key, val in pageranks.items():
    f.writerow([key, val])


# In[ ]:




