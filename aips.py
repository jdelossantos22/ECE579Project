import itertools
from graph import Edge, Node, Graph
import numpy as np
class Dispatcher(Node):
    def __init__(self, name="Dispatcher"):
        Node.__init__(self, name)
        return
    
    def addCustomers(self, customers, graph):
        self.customers = customers
        self.graph = graph
    
    def dispatch(self):
        #numBottles is number of bottles to be dispatched
        #instantiate the bottles
        numBottles = sum([c.replenishNum for c in self.needsDispatch])
        self.bottles = [Bottle for i in range(numBottles)]
        #call TSP method on customers list to be replenished
        self.graph.tsp_arr(self.needsDispatch)
        
        
    def checkCustomersReplenish(self):
        self.needsDispatch = []
        
        for c in self.customers:
            if c.checkShelves() == True:
                self.needsDispatch.append(c)
                
        print(self.needsDispatch)
        return len(self.needsDispatch)
        

class Customer(Node):
    
    def __init__(self, name):
        Node.__init__(self, name)
        self.emptyShelf = Shelf(2,0)
        self.fullShelf = Shelf(3,0)
        self.stand = Stand()
        self.replenish = True
        self.replenishNum = 3 #number of bottles to be replenished?
        
        
    def checkShelves(self):
        if self.fullShelf.curBottles <= 1:
            self.replenish = True
            return True
        elif self.stand.bottle.curVolume <= (1/4)*self.stand.bottle.capacity:
            self.replenish = True
            return True
        else: 
            return False
    def checkLeak(self):
        pass
        
class Shelf:
    def __init__(self, capacity, bottles=0):
        self.capacity = capacity
        self.curBottles = bottles
        #instantiates a bottle object in Shelf
        self.bottles = [Bottle() for i in range(self.curBottles)]
        return
    
    def addBottle(self, bottle):
        self.bottles.append(bottle)
        return
    
    def removeBottle(self, id):
        #remove bottle with id?
        
        self.bottles.remove(id)
        return id
        
    def getNum(self):
        return self.curBottles
    
class Stand:
    def __init__(self, bottle=None):
        self.bottle = bottle
        return
    
    def change(self, bottle):
        tempBottle = self.bottle
        bottle = bottle
        return tempBottle
        

class Chilled_Stand(Stand):
    def __init__(self):
        self.cooler = False
        self.threshold = 42.0
        self.dt = 2
        self.temperature = 42.0
        return
    def coolerOn(self):
        self.cooler = True
        return
    def coolerOff(self):
        self.cooler = False
    def increment(self):
        self.temperature += 1
    def decrement(self):
        self.temperature -= 1
    def checkTemp(self):
        if self.temperature >= self.threshold + self.dt:
            self.coolerOn()
        elif self.temperature <= self.threshold - self.dt:
            self.coolerOff()
        
    
    
class Bottle:
    newid = itertools.count()
    def __init__(self, type="Plastic", capacity=4.0):
        self.id = next(Bottle.newid)
        self.type = type #plastic(default) or clear glass
        self.capacity = capacity #4 gallons(default) or 6 gallons
        self.curVolume = 0.0 #initial state is empty shelves empty bottles
        self.curStand = "" #what is currStand
        
    def getId(self):
        return self.id
    def setType(self, type):
        self.type = type
    def getType(self):
        return self.type
    def setCapacity(self, capacity):
        self.capacity = capacity
    def getCapacity(self):
        return self.capacity
    def setCurVolume(self, v):
        self.curVolume = v
    def getCurVolume(self):
        return self.curVolume
    def decrementVol(self, val):
        self.curVolume -= val
    def incrementVol(self, val):
        self.curVolume += val

        
class Robot:
    def __init__(self):
        return
        
        
        
        
if __name__ == "__main__":
    customer = Customer("A")
    print(customer)
    

