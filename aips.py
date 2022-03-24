import itertools
class Customer:
    newid = itertools.count().next
    def __init__(self, name, id):
        self.name = name
        self.id = Customer.newid()
        self.emptyShelf = Shelf(2,0)
        self.fullShelf = Shelf(3,0)
        self.stand = Stand()
        self.replenish = True
        self.replenishNum = 0 #number of bottles to be replenished?
        
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
        return
    
    
class Bottle:
    newid = itertools.count().next
    def __init__(self, type="Plastic", capacity=4.0):
        self.id = Bottle.newid()
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
    
class Shelf:
    newid = itertools.count().next
    def __init__(self, type = "", numBottle=0, maxBottle=2):
        self.id = Shelf.newid()
        self.type = type
        self.numBottle=numBottle
        self.maxBottle=maxBottle
        
class Robot:
    def __init__(self):
        return
        
class Dispatcher:
    def __init__(self):
        return
    
    def dispatch(self, customers):
        #numBottles is number of bottles to be dispatched
        #instantiate the bottles
        numBottles = sum([c.replenishNum for c in customers])
        self.bottles = [Bottle for i in range(numBottles)]
        #call TSP method on customers list to be replenished
        

class Simulation:
    def __init__(self, customers):
        #needs customer(s)
        #needs edges(distance for each customer)
        self.customers = customers
        return
    
    def run(self):
        #pseudo-code for the states
        needsDispatch = []
        for c in self.customers:
            if self.checkShelves(c) == True:
                needsDispatch.append(c)
            checkStandTemp(c)
        return
    
    def checkShelves(self, c):
        if c.fullShelf.curBottles == 1 and \
            c.stand.bottle.curVolume <= (1/4)*c.stand.bottle.capacity:
                c.replenish = True
                return True
        else: 
            return False
        
    def checkStandTemp(self, c):
        #checking temperature of chilled stand
        return
    
    def checkForLeak(self, c):
        #check for leak
        return