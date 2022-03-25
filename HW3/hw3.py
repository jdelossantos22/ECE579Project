from asyncio import new_event_loop
from heapq import heappush, heappop
import copy
from mimetypes import init
from queue import PriorityQueue
import pandas as pd
import numpy as np
MOVES = [[-1,0,1],
         [-1,0,1]]
LEFT = (0,-1)
RIGHT = (0,1)
UP = (0,-1)
DOWN = (0,1)
MOVES = [LEFT,RIGHT,UP, DOWN]
class Graph:
    def __init__(self):
        return
    
class Node:
    def __init__(self, parent, state, empty_tile_pos, cost,heuristic, level):
        self.parent = parent
        self.state = state
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level
        self.a_score = cost+heuristic
        return
    def __lt__(self,nxt):
        return self.cost < nxt.cost
    
def euclidean(mat, goal):
    #heuristic #1
    #euclidena distance
    cost = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            location_in_goal = get_loc(goal, mat[i][j]) 
            dist_x = np.abs(i - location_in_goal[0])
            dist_y = np.abs(j-location_in_goal[1])
            cost += np.sqrt(dist_x^2 + dist_y^2)
    return cost

def manhattan(mat, goal):
    #heuristic #2
    #manhattan distance(number of tiles to goal)
    cost = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            location_in_goal = get_loc(goal, mat[i][j])
            cost += np.abs(i - location_in_goal[0]) + \
                np.abs(j-location_in_goal[1]) 
    return cost

def get_loc(goal,val):
    location = (0,0)
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if(goal[i][j] == val):
                return (i,j)
    return location
        
def printMatrix(mat):
    print(pd.DataFrame(mat).to_string(index=False, header=False))
    
def find_empty_tile(mat):
    location = (0,0)
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j] == -1):
                return (i,j)
    return location
            
    
def a_star(initial, goal, heuristic):
    #openList = []
    #closedList = []
    root = Node(None,
                initial,
                find_empty_tile(initial),
                0,
                heuristic(initial, goal),
                0)
    openList = PriorityQueue()
    print(heuristic(initial,goal))
    while not openList:
        #generate all children from current node
        #add to queue
        #sort queueu by a_score
        #call 
        continue
    return

def main():
    
    initialState = [[2,8,6],
                    [1,6,4],
                    [7,-1,5]]
    goalState = [[1,2,3],
                [8,-1,4],
                [7,6,5]]
    printMatrix(initialState)
    a_star(initialState, goalState, euclidean)
    a_star(initialState,goalState, manhattan)
    
    
if __name__ == "__main__":
    main()