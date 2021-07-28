"""
@author: Manny Torres
"""

import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
import math


def open_file(in_file,searchType):
	roadsList = []
	lat_lon_list = []

	with open(in_file, 'r') as words:

		if searchType == "bfs" or searchType == "dfs":
 #      for number, line in enumerate(lines, start = 6):
			for line, words in enumerate(words):
			
				if line > 74:
					mystring = words
					myString = re.sub(r"[\n\t\s]*", "", mystring)
					roadsList.append(myString.strip().split(','))
			
			print(" Full list: "+str(roadsList))

		if searchType == "A*":

			for line, words in enumerate(words):
				if line > 5 and line < 71:
					mystring = words
					myString = re.sub(r"[\n\t\s]*", "", mystring)
					lat_lon_list.append(myString.strip().split(','))

				if line > 74:
					mystring = words
					myString = re.sub(r"[\n\t\s]*", "", mystring)
					roadsList.append(myString.strip().split(','))

			roads_allinfo = combine(roadsList,lat_lon_list)
			roadsList = roads_allinfo
			print(" Full list: "+str(roads_allinfo))
		
	return roadsList
	
# Returns a master list with all the info in it
def combine(list1,list2):
	
		# Add lat lon to first city
		for i in list1:
			for j in list2:
				if i[0] == j[0]:
					i.append(j[1])
					i.append(j[2])

		# Add lat lon to second city		
		for k in list1:
			for l in list2:
				if k[1] == l[0]:
					k.append(l[1])
					k.append(l[2])

		# Add heuristic value between cities to list
		for comb in list1:
			comb.append(heuristic(float(comb[3]),float(comb[4]),float(comb[5]),float(comb[6])))
			#comb.append(heuristic(comb[3],comb[4],comb[5],comb[6]))

		# Add total cost H(n) + G(n) to list
		for tot in list1:
			hTotal = float(tot[2]) + float(tot[7])
			tot.append(hTotal)
			#comb.append(heuristic(comb[3],comb[4],comb[5],comb[6]))

		combined = list1
		
		return combined

# Returns heuristic value between source and a target cities given their geolocation
def heuristic(lat1,lon1,lat2,lon2):

#--
# Heuristic formula
# sqrt((69.5 * (Lat1 - Lat2)) ^ 2 + (69.5 * cos((Lat1 + Lat2)/360 * pi) * (Long1 - Long2)) ^ 2)
#--

	hval = math.sqrt(pow((69.5 * (lat1 - lat2)), 2) + pow(69.5 * math.cos((lat1 + lat2)/360 * math.pi) * (lon1 - lon2),2))

	return hval


def create_tree(node_list):
	
	df = pd.DataFrame(node_list, columns=['City1', 'City2', 'KM'])
	#call heuristic function here
	G = nx.from_pandas_edgelist(df, 'City1', 'City2')
	G = nx.from_pandas_edgelist(df, 'City1', 'City2', edge_attr='KM')
	
	return G

def create_tree_heuristics(node_list):
	
	df = pd.DataFrame(node_list, columns=['City1', 'City2', 'KM','Lat1','Lon1','Lat2','Lon2','H(n)','H(n)+G(n)'])
	#call heuristic function here
	G = nx.from_pandas_edgelist(df, 'City1', 'City2')
	G = nx.from_pandas_edgelist(df, 'City1', 'City2', edge_attr='KM')
	
	return G

# Determines the total cost of the path to goal
def cost(road_to_goal,info):

	total_cost = 0

	for i in range(len(road_to_goal)-1):
		print("City in path: "+str(road_to_goal[i]))
		for city in info:
			if ((road_to_goal[i] == city[0]) and (road_to_goal[i+1] == city[1])):
				total_cost += int(city[2])
			
			if ((road_to_goal[i] == city[1]) and (road_to_goal[i+1] == city[0])):
				print("Combo "+str(road_to_goal[i])+" - "+str(road_to_goal[i+1]))
				total_cost += int(city[2])

#		print("Total cost = "+str(total_cost))

	return total_cost



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
				
				break
				
			else:
				self.visited.append(s)  
				for neighbor in nList:
						if neighbor not in self.visited and neighbor not in self.stack:
							self.stack.append(neighbor)
							print("The stack is "+str(self.stack))
							self.iteration+=1

	
	def astar(self,node, goalCity, info):
		
#		print("info list: "+str(info))

		self.visited.append(node)
		self.queue.append(node)
		self.node = str(node)
		self.neighborList = (G.adj[node])
		self.iteration = 0
		
		options_w_values=[]
		self.cost = 0
				
		while self.queue:

			print("Queue at start of iteration " +str(self.iteration))
			print("Queue is "+str(self.queue))
			s = self.queue.pop()
			print("City to expand is: "+str(s))
			
			nList = self.getNeighbor(s)
			print("nList is "+str(nList))
			options_w_values=[]
			options=[]

			
			for cities in info:
			#	print("node is "+str(node)+", goal city is "+goalCity+" and cities is "+str(cities))
				for match_city in nList:
					
					if (s == cities[0] and match_city == cities[1]) or (s == cities[1] and match_city == cities[0]):
						options_w_values.append(cities)

			
			options_w_values.sort(key=lambda x:x[8], reverse=True)
			print("Sorted options"+str(options_w_values))
			
			for city_pos in options_w_values:
				if s == city_pos[0]:
					options.append(city_pos[1])
				
				else:
					options.append(city_pos[0])
		
			nList = options
			print("Updated nList is :"+str(nList))


			if (s == goalCity):
						#print("These are visited nodes\n >>>", self.visited, "\n")
						
						print("Found:", goalCity,"")
						self.return_path.append(goalCity)
						self.find_path(goalCity)
						print("Path to goal is "+str(self.return_path))
						self.cost = cost(self.return_path,info)
						print("Total cost/distance for this trip: "+str(self.cost))
						break
			else:
				self.visited.append(s)  
				for neighbor in nList:
					if neighbor not in self.visited and neighbor not in self.queue:
						self.queue.append(neighbor)
						print("The queue is "+str(self.queue))
						self.iteration+=1



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
				#print("Here is the path to the goal: ")
				#print(self.return_path)
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

	elif typeOfSearch == "A*":
		info = road_list
		g.astar(startCity, goalCity, info) 


if __name__ == "__main__":
	
	in_file = "Cities.txt"

	StartCity = "albanyNY"
	GoalCity = "omaha"
	#type_of_search = "bfs"
	#type_of_search = "dfs"
	type_of_search = "A*"

	road_list = open_file(in_file,type_of_search)

	print("Starting Node: " + StartCity)
	
	if type_of_search == "bfs" or type_of_search=="dfs":
		G = create_tree(road_list)

	elif type_of_search == "A*":
		G = create_tree_heuristics(road_list)
	
	callingSearch(StartCity, GoalCity, type_of_search)

	
	#print("Data frame is :"+str(G))
	
	nx.draw(G,
			  with_labels=True,
			  arrows=True)
	plt.show()
