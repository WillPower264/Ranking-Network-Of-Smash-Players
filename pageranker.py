# pageranker.py - Represents the PageRanking of a set of players given their game set

import pandas as pd
import networkx as nx
import numpy as np
import operator
import csv

class PageRanker:
    games = ""
    names = ""
    
    def __init__(self, games, names):
        self.games = pd.read_csv(games) # 6 column cleaned data
        self.names = pd.read_csv(names) # 2 column cleaned data
        
    def build_edgelist(self):
        data2 = self.games[['winner_global_id', 'loser_global_id']] # data with only IDs
        edgelist = []
        for i in range(0, len(data2)):
            edgelist.append(str(data2['winner_global_id'][i]) + ' '
                       + str(data2['loser_global_id'][i]))
        return data2
        
    def build_digraph(self, edgelist):
        g = nx.DiGraph()
        for i, row in edgelist.iterrows():
            g.add_edge(str(row[1]), str(row[0]), attr_dict=row[2:].to_dict())
        return g
    
    def pagerank(self, g):
        return nx.pagerank(g)

    def pagerank_sort(self, pr):
        return dict(sorted(pr.items(), key=operator.itemgetter(1),reverse=True))
    
    def pagerank_write(self, pr):
        f = csv.writer(open('pageranks.csv', 'w'))
        f.writerow(['ID', 'PageRank'])
        for key, val in pr.items():
            f.writerow([key, val])
            
    def id2name(self, id):
        try:
            return self.names['player'][list(names['id'][0:]).index(id)]
        except ValueError:
            return -1
        
    def name2id(self, name):
        try:
            return self.names['id'][list(names['player'][0:]).index(name)]
        except ValueError:
            return -1

    def leaderboard(self, n):
        ranks = pd.read_csv('pageranks.csv')
        print("Leaderboard:")
        board = np.array([['Rank', 'Player', 'ID']])
        for i in range(0, n):
            board = np.append(board, [[i, self.id2name(ranks['ID'][i]), str(ranks['ID'][i])]], axis=0)
            #print('Rank: ' + str(i) + ' - Player: ' + self.id2name(ranks['ID'][i]) + ' - ID: ' + str(ranks['ID'][i]))
        return board
            
    def id2rank(self, id):
        ranks = pd.read_csv('pageranks.csv')
        return list(ranks['ID']).index(id)