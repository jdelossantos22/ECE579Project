from aips import *
from graph import Graph, Node, Edge
from restack import *
import time
import random
import itertools
import string

class Simulation:
    def __init__(self, numCustomers=0):
        #needs customer(s)
        #needs edges(distance for each customer)
        print(f"This simulation will have {numCustomers} customers.")
        self.numCustomers = int(numCustomers)
        self.customers = []
        self.graph = Graph()
        self.dispatcher = Dispatcher()
        self.graph.add_node(self.dispatcher)
        
        return
    
    def __str__(self):
        pass
    
    def add_customer(self, customer):
        self.customers.append(customer)
        self.graph.add_node(customer)
    
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
        #generator 
        #yield 
        
        while(True):
            output = ""
            num = self.dispatcher.checkCustomersReplenish()
            if (num > 0): #we need to deliver water bottles
                self.dispatcher.dispatch()
                #output += self.dispatcher.dispatch()
            
            
            for c in self.customers:
                #Step #3.b Check dispenser temperature
                temperature, status  = c.chilledStand.checkTemp()
                print(f'{str(c)} chilled stand is at {temperature} °F and the cooler is \
                      {"ON" if status else "OFF"}')
                #output += ^^^
                #Step #4 call restack on every iteration of while loop
                c.checkDelivered() #check if restack is needed
                c.robot.restack(c.fullShelf.bottles, c.stand.bottle, c.emptyShelf.bottles) #restack anyway
                
            time.sleep(1)
            #yield output
        
        
    
def main():
    numCust = input("Please enter the number of customers for simulation: ")
    s = Simulation(numCust)
    s.process()
    s.run()
        

if __name__ == "__main__":
    main()