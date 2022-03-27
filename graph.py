import itertools
class Edge:
    def __init__(self,a,b, distance):
        self.a = a
        self.b = b
        self.distance=distance
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
class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def add_node(self,node):
        self.nodes.append(node)
    def add_edge(self,a,b,dist):
        e = Edge(a,b,dist)
        self.edges.append(e)