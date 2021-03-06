# ECE 479/579 Principle of Artificial Intelligence
# Homework 3
# Jero Delos Santos, Almutasim Alanazi, Kevin Grady
# Note: The algorithm for the 8-puzzle setup and movement is adapted from the credited code:
# https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288

import numpy as np
import time
from copy import deepcopy

class Node:
    def __init__(self, data, level, fval):
        # Creation of Node class with the data, level, and fval
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        # Creates the children of current node through all possible 8-puzzle moves
        x,y = np.where(np.asarray(self.data) == "_")
        x,y = x[0], y[0]
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in val_list:
            child = self.checkValidMove(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children
        
    def checkValidMove(self,puz,x1,y1,x2,y2):
        # Checks to see that the proposed move does not move the blank off the board.
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = deepcopy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

class Puzzle:
    def __init__(self,size, heuristic):
        self.n = size
        # Nodes that we have not explored yet.
        self.open = []
        # Nodes that have children generated for already.
        self.closed = []
        # Manhattan and Euclidean heuristics chosen here.
        self.heuristic = heuristic

    def process(self):
        # Take in the 8-puzzle start state.
        print("Enter the 8-puzzle's beginning state\n")
        startState = []
        for i in range(0, self.n):
            singleVal = input().split(" ")
            startState.append(singleVal)    
        goal = [["1","2", "3"], ["8", "_", "4"], ["7", "6", "5"]]
        startState = Node(startState, 0, 0)
        startState.fval = self.calc_f(startState, goal)
        # Our start node exists as an explored node to begin with.
        self.open.append(startState)
        print("\n\n")
        maxLevel = 0
        
        while True:
            cur = self.open[0]
            # Prints the current 8-puzzle board state to terminal.
            print("\n")
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            
            # If the estimated cost to the goal node is 0, then our current node is the goal node.
            if(self.heuristic(cur.data,goal) == 0):
                break
            # We are not yet at the goal node. Create children nodes for the current node given all possible moves.
            for i in cur.generate_child():
                # Each child node gets an associated cost which is estimated as the current cost plus the estimated cost
                # of the child node to the goal node.
                i.fval = self.calc_f(i,goal)
                # If the child node's level is greater than the current max level, then our global max level variable
                # is incremented. maxLevel should always represent the deepest node's level in the current search.
                if i.level > maxLevel:
                    maxLevel = i.level
                # The open list gets the current child node, and we move onto the next child node.
                self.open.append(i)
            # The closed list gets the current node of which we just evaluated all children at appended to it.
            self.closed.append(cur)
            del self.open[0]
            # Sorts the f values in increasing order for each child node of our current node.
            self.open.sort(key = lambda x:x.fval,reverse=False)
        print(f"The # of levels of the algorithm is {maxLevel}")
        
    def calc_f(self,start,goal):
        # f(x) = h(x) + g(x)
        hx = self.heuristic(start.data, goal)
        gx = start.level
        return hx + gx

    
    
    
def euclidean(mat, goal):
    #heuristic #1
    #euclidean distance using pythagorean theorem
    cost = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            location_in_goal = get_loc(goal, mat[i][j]) 
            dist_x = np.abs(float(i) - location_in_goal[0])
            dist_y = np.abs(float(j)-location_in_goal[1])
            cost += np.sqrt(dist_x**2 + dist_y**2)
    return cost

def manhattan(mat, goal):
    #heuristic #2
    #manhattan distance (number of individual tiles to goal)
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

def main():
    start_time = time.time()
    puz = Puzzle(3, euclidean)
    puz.process()
    print("--- %s milliseconds ---" % (time.time() - start_time))
    start_time = time.time()
    puz = Puzzle(3, manhattan)
    puz.process()
    print("--- %s milliseconds ---" % (time.time() - start_time))
    
if __name__ == "__main__":
    main()
