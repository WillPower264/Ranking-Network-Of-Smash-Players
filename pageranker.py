# pageranker.py - Represents the PageRanking of a set of players given their game set

import pandas as pd
import networkx as nx
import numpy as np
import operator
import csv

class PageRanker:
    games = ""
    names = ""
    startDate = 0
    endDate = 0
    weighted = False
    
    # startDate and endDate (both in Unix time) mark the bounds of the time period of interest
    # weighted is true iff we want each game to form an edge; if false, each edge represents a set
    def __init__(self, games, names, startDate = 0, endDate = float("inf"), weighted = 0):
        self.games = pd.read_csv(games)
        self.names = pd.read_csv(names)
        self.startDate = startDate
        self.endDate = endDate
        self.weighted = weighted
        
    def build_edgelist(self):
        edgelist = []
        if self.weighted:
            data2 = self.games[['winner_global_id', 'loser_global_id', 'endDate', 'winner_score', 'loser_score']]
            for i in range(0, len(data2)):
                if data2['endDate'][i] >= self.startDate and data2['endDate'][i] <= self.endDate:
                    for j in range(0, data2['winner_score'][i]):
                        edgelist.append((str(data2['winner_global_id'][i]), str(data2['loser_global_id'][i])))
                    for j in range(0, data2['loser_score'][i]):
                        edgelist.append((str(data2['loser_global_id'][i]), str(data2['winner_global_id'][i])))
        else:
            data2 = self.games[['winner_global_id', 'loser_global_id', 'endDate']] # data with only IDs
            for i in range(0, len(data2)):
                if data2['endDate'][i] >= self.startDate and data2['endDate'][i] <= self.endDate:
                    edgelist.append((str(data2['winner_global_id'][i]), str(data2['loser_global_id'][i])))
            
        return edgelist

    def build_digraph(self, edgelist):
        g = nx.DiGraph()
        for row in edgelist:
            g.add_edge(str(row[1]), str(row[0]))
        return g
    
    def pagerank(self, g):
        return nx.pagerank(g)

    def pagerank_sort(self, pr):
        return dict(sorted(pr.items(), key=operator.itemgetter(1),reverse=True))
    
    def pagerank_write(self, pr, filename):
        f = csv.writer(open(filename, 'w'))
        f.writerow(['ID', 'PageRank'])
        for key, val in pr.items():
            f.writerow([key, val])
            
    def id2name(self, id):
        try:
            return self.names['player'][list(self.names['id'][0:]).index(id)]
        except ValueError:
            return -1
        
    def name2id(self, name):
        try:
            return self.names['id'][list(self.names['player'][0:]).index(name)]
        except ValueError:
            return -1
        
    def id2rank(self, id, filename):
        ranks = pd.read_csv(filename)
        return list(ranks['ID']).index(id)

    def leaderboard(self, n, filename):
        ranks = pd.read_csv(filename)
        print("Leaderboard:")
        board = np.array([['Rank', 'Player', 'ID']])
        for i in range(0, n):
            board = np.append(board, [[i, self.id2name(ranks['ID'][i]), str(ranks['ID'][i])]], axis=0)
        return board
            
