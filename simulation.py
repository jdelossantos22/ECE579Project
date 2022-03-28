from aips import *
from graph import Graph, Node, Edge
from Re_stack_the_full_bottle_shelf import *
import time
import simpy
import random
import itertools

class Simulation:
    def __init__(self, numCustomers):
        #needs customer(s)
        #needs edges(distance for each customer)
        print(f"This simulation will have {numCustomers} customers.")
        self.numCustomers = int(numCustomers)
        return
    def process(self):
        #input from user
        self.dispatcher = Dispatcher()
        self.customers = []
        self.graph = Graph()
        self.graph.add_node(self.dispatcher)
        for i in range(self.numCustomers):
            c = Customer(input(f'Please enter name for customer {i}: '))
            self.customers.append(c)
            self.graph.add_node(c)
        #build graph
        #initialize
        cCombination = itertools.combinations(self.customers,2)
        
        
        for c in self.customers:
            dist = input(f"Please enter distance between {str(c)} and {str(self.dispatcher)}: ")
            self.graph.add_edge(self.dispatcher,c,dist)
            
        #print(list(cCombination))
        for c in list(cCombination):
            cust1 = c[0]
            cust2 = c[1]
            dist = input(f"Please enter distance between {str(cust1)} and {str(cust2)}: ")
            self.graph.add_edge(cust1,cust2,dist)
            
        #for n in self.graph.nodes:
        #    print(n.id)
            
        self.dispatcher.addCustomers(self.customers, self.graph)
        
    def run(self):
        #pseudo-code for the states
        num = self.dispatcher.checkCustomersReplenish()
        if (num > 0):
            self.dispatcher.dispatch()
    
def main():
    numCust = input("Please enter the number of customers for simulation: ")
    s = Simulation(numCust)
    s.process()
    s.run()
        

if __name__ == "__main__":
    main()