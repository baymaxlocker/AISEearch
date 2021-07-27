"""
@author: Manny Torres
"""

import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt


def open_file(in_file):
    roadsList = []

    with open(in_file, 'r') as words:
#        for line in words:
        lines = words
        
 #      for number, line in enumerate(lines, start = 6):
        for line, words in enumerate(words):
            
            if line > 5 and line <71:
                mystring = words
                myString = re.sub(r"[\n\t\s]*", "", mystring)
                roadsList.append(myString.strip().split(','))
        
        print("Here's the road list: "+str(roadsList))
        
    return roadsList


def create_tree(node_list):
    
    df = pd.DataFrame(node_list, columns=['City1', 'City2', 'KM'])
    #call heuristic function here
    G = nx.from_pandas_edgelist(df, 'City1', 'City2')
    G = nx.from_pandas_edgelist(df, 'City1', 'City2', edge_attr='KM')
    
    return G


class Node(object):
    def __init__(self, parent, name):
        #self.parent = parent
        self.name = name


class Search(Node):
    def __init__(self):
        self.visited = []
        self.queue = []
        self.weightedQueue = {}
        self.newNodes = []
        self.neighborL = []
        self.return_path = []
        self.stack=[]

    def bfs(self, node, goalCity):
        self.visited.append(node)
        self.queue.append(node)
        self.node = str(node)
        self.neighborList = (G.adj[node])
        while self.queue:
            s = self.queue.pop(0)
            print("City to expand is: "+str(s))
            nList = self.getNeighbor(s)
            if (s == goalCity):
                        #print("These are visited nodes\n >>>", self.visited, "\n")
                        
                        print("Found:", goalCity,"")
                        self.return_path.append(goalCity)
                        self.find_path(goalCity)
                        print("Return path is "+str(self.return_path))
                        break
            else:
                self.visited.append(s)  
                for neighbor in nList:
                    if neighbor not in self.visited and neighbor not in self.queue:
                        self.queue.append(neighbor)
                        print("The stack is "+str(self.queue))
     
    def dfs(self, node, goalCity):
        self.visited.append(node)
        self.stack.append(node)
        self.node = str(node)
        self.neighborList = (G.adj[node])
        self.iteration = 0
        while self.stack:
            s = self.stack.pop()
            nList = self.getNeighbor(s)
            if (s == goalCity):
             #print("These are visited nodes\n >>>", self.visited, "\n")
                   
                print("Found:", goalCity,"")
                self.return_path.append(goalCity)
                self.find_path(goalCity)
                print("Return path is "+str(self.return_path))
                break
                
            else:
                self.visited.append(s)  
                for neighbor in nList:
                        if neighbor not in self.visited and neighbor not in self.stack:
                            self.stack.append(neighbor)
                            print("The stack is "+str(self.stack))
                            self.iteration+=1

    def astar(self,f):
        print("Group 7 is awesome!")

# procedure DFS_iterative(G, v) is
#     let S be a stack
#     S.push(iterator of G.adjacentEdges(v))
#     while S is not empty do
#         if S.peek().hasNext() then
#             w = S.peek().next()
#             if w is not labeled as discovered then
#                 label w as discovered
#                 S.push(iterator of G.adjacentEdges(w))
#         else
#             S.pop() 



    def getNeighbor(self, CurrNode):
        new_nodes = []
        inpt = str(CurrNode)
        neighbor = list(G.adj[inpt])
        for n in neighbor:
            if n not in self.queue:
                if n not in self.visited:
                    new_nodes.append(n)
                    
        newNeighbor = new_nodes
        self.neighborL.append(new_nodes)
        return newNeighbor    


    def find_path(self, goalCity):
        currNode = goalCity
        neighbor = list(G.adj[currNode])
        
        for n in neighbor:
            if n == self.visited[0]:
                self.return_path.insert(0, n)
                print("Here is the path to the goal")
                print(self.return_path)
                break
         
            if n in self.visited and n not in self.return_path:
                self.return_path.insert(0, n)
                self.find_path(n)
                if self.return_path[0] == self.visited[0]:
                    break
            



def callingSearch(startCity, goalCity, typeOfSearch):
    g = Search()
    if typeOfSearch == "bfs":
        g.bfs(startCity, goalCity)   
    
    elif typeOfSearch == "dfs":
        g.dfs(startCity, goalCity) 


if __name__ == "__main__":
    
    in_file = "Cities.txt"

    StartCity = "albanyNY"
    GoalCity = "omaha"
    type_of_search = "bfs"
    #type_of_search = "dfs"

    road_list = open_file(in_file)
    G = create_tree(road_list)
    print("Data frame is :"+str(G))
    nx.draw(G,
              with_labels=True,
              arrows=True)
    plt.show()
    print("Starting Node: " + StartCity)
    callingSearch(StartCity, GoalCity, type_of_search)