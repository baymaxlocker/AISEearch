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



if __name__ == "__main__":
    
    in_file = "Cities.txt"

    StartCity = "albanyNY"
    GoalCity = "omaha"
    type_of_search = "bfs"
    #type_of_search = "dfs"

    road_list = open_file(in_file)
    # G = create_tree(road_list)
    # print("Data frame is :"+str(G))
    # nx.draw(G,
    #           with_labels=True,
    #           arrows=True)
    # plt.show()
    # print("Starting Node: " + StartCity)
    # callingSearch(StartCity, GoalCity, type_of_search)