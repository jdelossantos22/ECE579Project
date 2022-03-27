import itertools
class Edge:
    def __init__(self,a,b, distance):
        self.distance=distance
        return

class Node:
    newid = itertools.count().next
    def __init__(self,name):
        self.id = Node.newid()
        self.name = name
        
class Graph:
    def __init__(self):
        pass