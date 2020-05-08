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
    
    def __init__(self, games, names, startDate, endDate):
        self.games = pd.read_csv(games) # 4 column cleaned data
        self.names = pd.read_csv(names) # 2 column cleaned data
        self.startDate = startDate
        self.endDate = endDate
        
    def build_edgelist(self):
        data2 = self.games[['winner_global_id', 'loser_global_id', 'startDate']] # data with only IDs
        edgelist = []
        for i in range(0, len(data2)):
            if data2['startDate'][i] >= self.startDate and data2['startDate'][i] <= self.endDate:
                edgelist.append((str(data2['winner_global_id'][i]), str(data2['loser_global_id'][i])))
        return edgelist
    
    def build_edgelist_weighted(self):
        data2 = self.games[['winner_global_id', 'loser_global_id', 'winner_score', 'loser_score']]
        edgelist = []
        for i in range(0, len(data2)):
            if data2['startDate'][i] >= self.startDate and data2['startDate'][i] <= self.endDate:
                for j in range(0, data2['winner_score'][i]):
                    edgelist.append((str(data2['winner_global_id'][i]), str(data2['loser_global_id'][i])))
                for j in range(0, data2['loser_score'][i]):
                    edgelist.append((str(data2['loser_global_id'][i]), str(data2['winner_global_id'][i])))
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
    
    def pagerank_write(self, pr):
        f = csv.writer(open('pageranks.csv', 'w'))
        f.writerow(['ID', 'PageRank'])
        for key, val in pr.items():
            f.writerow([key, val])
            
    def pagerank_write_weighted(self, pr):
        f = csv.writer(open('pageranks_weighted.csv', 'w'))
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

    def leaderboard(self, n):
        ranks = pd.read_csv('pageranks.csv')
        print("Leaderboard:")
        board = np.array([['Rank', 'Player', 'ID']])
        for i in range(0, n):
            board = np.append(board, [[i, self.id2name(ranks['ID'][i]), str(ranks['ID'][i])]], axis=0)
            #print('Rank: ' + str(i) + ' - Player: ' + self.id2name(ranks['ID'][i]) + ' - ID: ' + str(ranks['ID'][i]))
        return board
    
    def leaderboard_weighted(self, n):
        ranks = pd.read_csv('pageranks_weighted.csv')
        print("Leaderboard:")
        board = np.array([['Rank', 'Player', 'ID']])
        for i in range(0, n):
            board = np.append(board, [[i, self.id2name(ranks['ID'][i]), str(ranks['ID'][i])]], axis=0)
            #print('Rank: ' + str(i) + ' - Player: ' + self.id2name(ranks['ID'][i]) + ' - ID: ' + str(ranks['ID'][i]))
        return board
            
    def id2rank(self, id):
        ranks = pd.read_csv('pageranks.csv')
        return list(ranks['ID']).index(id)