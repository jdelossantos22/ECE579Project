import itertools
from re import A
import numpy as np
from TSP.tsp import tsp
from tsp import *
class Edge:
    def __init__(self,a,b, distance):
        self.a = a
        self.b = b
        self.distance=float(distance)
        return
    def __repr__(self):
        return f'{self.a} - {self.b} = {self.distance}'
    def __str__(self):
        return f'{self.a} - {self.b} = {self.distance}'

class Node:
    newid = itertools.count()
    def __init__(self,name):
        self.id = next(Node.newid)
        self.name = name
        
    def __repr__(self):
        return str(self.id)
    def __str__(self):
        return self.name
    def __eq__(self,other):
        return self.id == other.id
    
class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def add_node(self,node):
        self.nodes.append(node)
    def add_edge(self,a,b,dist):
        e = Edge(a,b,dist)
        self.edges.append(e)
        
    def convertTo2d(self,arr, size):
        tempArr = []
        j = 0
        for i in range(0,len(arr),size):
            temp = arr[i:i+size]
            tempArr.append(temp)
        
        return tempArr
    
    def get_dist(self,a,b):
        for e in self.edges:
            if e.a == a and e.b == b or \
                e.a == b and e.b == a:
                    return e.distance
        return 0
        
    def tsp_arr(self, newNodes):
        #[print(type(x)) for x in newNodes]
        print("Finding optimal route via TSP")
        newNodes.insert(0,self.nodes[0]) #inserting dispatcher at the beginning
        #print(newNodes)
        #permuations of nodes
        tsp_perm = [n for n in itertools.product(newNodes, repeat=2)]
        #print(tsp_perm)
        tsp_perm = self.convertTo2d(tsp_perm, len(newNodes))
        #print(tsp_perm)
        tsp_dist = []
        for i in range(len(tsp_perm)):
            tsp_dist_row = []
            for j in range(len(tsp_perm[i])):
                tsp_dist_row.append(int(self.get_dist(tsp_perm[i][j][0], tsp_perm[i][j][1])))
                
            tsp_dist.append(tsp_dist_row)
        #print(tsp_dist)
        (Optimal_PathLength,Best_Route) = tsp(tsp_dist)
        print("The shortest possible length distance is : ", Optimal_PathLength)
        print("The optimal path is : ", end="")
        [print(newNodes[i], end=" -> ") for i in Best_Route[:-1]]
        print(self.nodes[Best_Route[-1]])
        return (Optimal_PathLength,[newNodes[i] for i in Best_Route])
        