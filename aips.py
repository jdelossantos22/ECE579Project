from copy import deepcopy
import itertools
from venv import create
from graph import Edge, Node, Graph
import numpy as np
import datetime
import time
import restack

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
        self.bottles = [Bottle(curVolume=4.0) for i in range(numBottles)]
        #call TSP method on customers list to be replenished
        print(f"The following customers needs replenishing: {self.needsDispatch}")
        (Optimal_PathLength,Best_Route) = self.graph.tsp_arr(self.needsDispatch)
        print(type(Best_Route))
        Route_Customers = Best_Route[1:-1]
        print("Dispatcher is starting their delivery")
        for c in Route_Customers:
            #adding bottles to shelf and also removing bottle object from list to be delivered
            full = [c.fullShelf.addBottle(self.bottles.pop(0)) for n in range(c.replenishNum)]
            c.replenish = False if full else True #checking if Full Shelf is full
            c.delivery = True
            print(f'{c.replenishNum} bottles has been delivered to {c}')
        
        
    def checkCustomersReplenish(self):
        print("Checking which customers needs to be replenished")
        self.needsDispatch = []
        
        for c in self.customers:
            if c.checkShelves() == True:
                #print(type(c))
                self.needsDispatch.append(c)
                
        #print(self.needsDispatch)
        return len(self.needsDispatch)
    
        

class Customer(Node):
    
    def __init__(self, name):
        Node.__init__(self, name)
        
        self.emptyShelf = Shelf(2,0)
        self.fullShelf = Shelf(3,0)
        self.stand = Stand()
        self.chilledStand = Chilled_Stand()
        self.robot = Robot()
        
        self.replenish = True
        self.replenishNum = 3 #number of bottles to be replenished?
        self.delivery = True #there has been a delivery used to call robot restack
        
        
        
    def checkShelves(self):
        if self.fullShelf.curBottles <= 1:
            self.replenish = True
            return True
        elif self.stand.bottle.curVolume <= (1/4)*self.stand.bottle.capacity:
            self.replenish = True
            return True
        else: 
            return False
        
    def checkDelivered(self):
        if self.delivery:
            if self.robot.restack(): #if restacking is successful
                self.delivery = False
            
        
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
        bottle.delivered()
        self.bottles.append(bottle)
        print(f'Added Bottle {str(bottle)}')
        self.curBottles = len(self.bottles)
        return True if self.curBottles == self.capacity else False
    
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
        self.decrement() if self.cooler else self.increment()
        return self.temperature, self.cooler
        
    
    
class Bottle:
    newid = itertools.count()
    def __init__(self, type="Plastic", capacity=4.0, curVolume=4.0):
        self.id = next(Bottle.newid)
        self.type = type #plastic(default) or clear glass
        self.capacity = capacity #4 gallons(default) or 6 gallons
        self.curVolume = curVolume #initial state is empty shelves empty bottles
        self.curStand = "" #what is currStand
        self.createdAt = datetime.datetime.utcnow()
        self.deliveredAt = None
        time.sleep(0.001)
        
    def __str__(self):
        return f'{str(self.id)} : {self.createdAt} : {self.deliveredAt}'
    
    def __repr__(self):
        return str(self.id)
    
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
    def delivered(self):
        self.deliveredAt = datetime.datetime.utcnow()
        time.sleep(0.001)
    def empty(self):
        return True if self.curVolume == 0.0 else False

        
class Robot:
    newid = itertools.count()
    def __init__(self):
        self.id = next(Bottle.newid)
    
    #call restack here
    def restack(self, bottles, onStand):
        #deliverySorted = sorted(bottles, key=lambda x: x.deliveredAt) #delivery matters for the initial state
        deliverySorted = bottles
        createdSorted = sorted(bottles, key=lambda x : x.createdAt, reverse=True) #created matters for the goal state
        print(deliverySorted)
        print(createdSorted)
        
        on_states = []
        for i in range(len(deliverySorted)):
            try:
                on_states.append(restack.ON(deliverySorted[i+1], deliverySorted[i]))
            except IndexError:
                continue
        onstandState = restack.ONSHELFSTAND(onStand)
        topBottleState = restack.TOPBOTTLE(deliverySorted[-1])
        initialState = deepcopy(on_states)#[[on_states, onstandState, topBottleState, restack.ARMEMPTY()]]
        initialState.append(onstandState)
        initialState.append(topBottleState)
        initialState.append(restack.ARMEMPTY())
        print(initialState)
        print(on_states)
        
        on_states = []
        
        #if the bottle on stand is empty replace it with the oldest water on the shelf
        lenOnStand = len(createdSorted) - 1 if onStand.empty() else len(createdSorted)
        onStand = createdSorted[-1] if onStand.empty() else onStand
        
        for i in range(lenOnStand):
            try:
                on_states.append(restack.ON(createdSorted[i+1], createdSorted[i]))
            except IndexError:
                continue
        goalState = deepcopy(on_states)
        goalState.append(restack.ONSHELFSTAND(onStand))
        goalState.append(restack.TOPBOTTLE(createdSorted[lenOnStand-1]))
        goalState.append(restack.ARMEMPTY())
        
        print(goalState)
        
        goal_stack = restack.GoalStackPlanner(initial_state=initialState, goal_state=goalState)
        steps = goal_stack.get_steps()

        print(steps)
        last_element = [steps[-6], steps[-5]]

        for x in last_element:
            steps.append(x)
        
        return True
        
        
        
        
        
if __name__ == "__main__":
    onstand = Bottle()
    bottles = []
    for i in range(3):
        bottles.append(Bottle())
    [b.delivered() for b in bottles]    
    [print(b) for b in bottles]
    
    robot = Robot()
    robot.restack(bottles, onstand)
    
    

