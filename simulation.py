from aips import *
from graph import Graph, Node, Edge
from restack import *
import time
import simpy
import random
import itertools
import string

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
            name = input(f'Please enter name for customer {i}: ')
            if name == "":
                name = random.choice(string.ascii_letters)
            c = Customer(name)
            self.customers.append(c)
            self.graph.add_node(c)
        #build graph
        #initialize
        cCombination = itertools.combinations(self.customers,2)
        
        
        for c in self.customers:
            dist = input(f"Please enter distance between {str(c)} and {str(self.dispatcher)}: ")
            dist = random.uniform(1, 50) if dist == "" else dist
                
            self.graph.add_edge(self.dispatcher,c,float(dist))
            
        #print(list(cCombination))
        for c in list(cCombination):
            cust1 = c[0]
            cust2 = c[1]
            dist = input(f"Please enter distance between {str(cust1)} and {str(cust2)}: ")
            dist = random.uniform(1, 50) if dist == "" else dist
            self.graph.add_edge(cust1,cust2,float(dist))
            
        #for n in self.graph.nodes:
        #    print(n.id)
            
        self.dispatcher.addCustomers(self.customers, self.graph)
        
    def run(self):
        #pseudo-code for the states
        while(True):
            num = self.dispatcher.checkCustomersReplenish()
            if (num > 0):
                self.dispatcher.dispatch()
            #Step #4 call restack on every iteration of while loop
            
            #Step #3.b Check dispenser temperature
            for c in self.customers:
                temperature, status  = c.chilledStand.checkTemp()
                print(f'{str(c)} chilled stand is at {temperature} °F and the cooler is {"ON" if status else "OFF"}')
            time.sleep(1)
        
        
    
def main():
    numCust = input("Please enter the number of customers for simulation: ")
    s = Simulation(numCust)
    s.process()
    s.run()
        

if __name__ == "__main__":
    main()