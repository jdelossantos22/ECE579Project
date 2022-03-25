from heapq import heappush, heappop
import copy
import pandas as pd
import numpy as np
MOVES = [[-1,0,1],
         [-1,0,1]]
class Graph:
    def __init__(self):
        return
    
class Node:
    def __init__(self, parent, state, empty_tile_pos, cost, level):
        self.parent = parent
        self.state = state
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level
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
    
def a_star(initial, goal, heuristic):
    print(heuristic(initial,goal))
    return

def main():
    openList = []
    closedList = []
    initialState = [[2,8,6],
                    [1,6,4],
                    [7,-1,5]]
    goalState = [[1,2,3],
                [8,-1,4],
                [7,6,5]]
    printMatrix(initialState)
    a_star(initialState, goalState, manhattan)
    
    
if __name__ == "__main__":
    main()