from copy import deepcopy
import itertools
from venv import create
from graph import Edge, Node, Graph
import numpy as np
import datetime
import time
import restack 
import random

LEAK_PERCENTAGE = 0.2

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
        
        # Drink amount varies from 0.1 to 0.3 whenever the i_count mod 5 == 0
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
        
        
    def checkCustomersReplenishLeak(self):
        print("Checking which customers needs to be replenished or have a leak")
        self.needsDispatch = []
        
        for c in self.customers:
            if c.checkShelves() == True or c.checkLeak() == True:
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
        
        # Assuming only the bottle currently in the water stand can have a leak
        # ie, customer can only have 1 leak at a time, so not a bottle attribute
        self.leak = False
        
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
                
    def deliveryArrived(self):
        self.delivery = True
        
    def checkLeak(self):
        return self.leak
    
    def generateLeak(self, percentage):
        bottleList = self.fullShelf.bottles
        bottleList.append(self.chilledStand.bottle)
        
        for bottle in bottleList:
            chance = random.random()
            if chance < percentage:
                bottle.leakBool = True
    
    def consumeWater(self):
        self.chilledStand.bottle.decrementVol(random.random()*self.chilledStand.bottle.capacity)
        self.chilledStand.bottle.lastCheckedVol = self.chilledStand.bottle.curVolume
        
    def detectLeak(self):
        bottleList = self.fullShelf.bottles
        bottleList.append(self.chilledStand.bottle)
        #leak = False
        output = ""
        for bottle in bottleList:
            if bottle.curVolume != bottle.lastCheckedVol:
                bottle.leakBool = True
                output += f"{self.name}: Bottle {bottle.id} has a leak\n"
                
        print(output)
        return output
                
    
        
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
    
    def drink(self):
        vol = random.random() * self.bottle.capacity
        self.bottle.decrementVol(vol)
        return vol
        

class Chilled_Stand(Stand):
    def __init__(self):
        super().__init__()
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
        self.leakBool = False
        self.lastCheckedVol = curVolume
        time.sleep(0.001)
        
    def __str__(self):
        return f'{str(self.id)}'
    
    def __repr__(self):
        return str(self.id)
    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ == other.__class__
    
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
    def leak(self):
        self.leakBool = True if random.random() < LEAK_PERCENTAGE else False
        return self.leakBool

        
class Robot:
    newid = itertools.count()
    def __init__(self):
        self.id = next(Robot.newid)
    
    #call restack here
    def restack(self, bottles, onStand, emptyShelf=[]):
        #deliverySorted = sorted(bottles, key=lambda x: x.deliveredAt) #delivery matters for the initial state
        deliverySorted = bottles #bottom to top
        createdSorted = sorted(bottles, key=lambda x : x.createdAt, reverse=True) #created matters for the goal state #newest to oldest
        print(deliverySorted)
        print(createdSorted)
        
        on_states = []
        for i in range(len(deliverySorted)):
            try:
                on_states.append(restack.ON(deliverySorted[i+1], deliverySorted[i]))
            except IndexError:
                continue
            
        
        topBottleState = restack.TOPBOTTLE(deliverySorted[-1])
        initialState = deepcopy(on_states)#[[on_states, onstandState, topBottleState, restack.ARMEMPTY()]]
        initialState.append(restack.ONTABLE(deliverySorted[0]))
        
        if isinstance(onStand, Bottle):
            onstandState = restack.ONSHELFSTAND(onStand) 
            initialState.append(onstandState)
            initialState.append(restack.TOPBOTTLE(onStand))
        
        #empty shelf initial state
        if len(emptyShelf) > 0:
            for i in range(len(emptyShelf)):
                try:
                    initialState.append(restack.ON(emptyShelf[i+1], emptyShelf[i]))
                except IndexError:
                    continue
            initialState.append(restack.ONTABLE(emptyShelf[0]))
            initialState.append(restack.TOPBOTTLE(emptyShelf[-1]))
        
        initialState.append(topBottleState)
        initialState.append(restack.ARMEMPTY())
        print(initialState)
        #print(on_states)
        
        on_states = []
        
        #if the bottle on stand is empty replace it with the oldest water on the shelf
        #lenOnStand = len(createdSorted) - 1 if onStand.empty() else len(createdSorted)
        #onStand = createdSorted[-1] if onStand.empty() else onStand
        
        if not isinstance(onStand, Bottle): #if there are no onstand
            onstandState = restack.ONSHELFSTAND(createdSorted[-1])
            clearOnStand = restack.TOPBOTTLE(createdSorted[-1])
            lenOnStand = len(createdSorted) - 2 
            topBottle = createdSorted[-2]
        elif onStand.empty():
            onstandState = restack.ONSHELFSTAND(createdSorted[-1]) # on stand should be the oldest bottle in the full shelf
            clearOnStand = restack.TOPBOTTLE(createdSorted[-1]) 
            lenOnStand = len(createdSorted) - 2 
            topBottle = createdSorted[-2]
            emptyShelf.append(onStand) #emptyshelf needs to be added
        else:
            onstandState = restack.ONSHELFSTAND(onStand)
            clearOnStand = restack.TOPBOTTLE(createdSorted[-1])
            lenOnStand = len(createdSorted)
            topBottle = createdSorted[-1]
        
        for i in range(lenOnStand):
            try:
                on_states.append(restack.ON(createdSorted[i+1], createdSorted[i]))
            except IndexError:
                continue
            
        goalState = deepcopy(on_states)
        goalState.append(onstandState)
        goalState.append(clearOnStand)
        goalState.append(restack.ONTABLE(createdSorted[0]))
        goalState.append(restack.TOPBOTTLE(topBottle))
        goalState.append(restack.ARMEMPTY())
        
        
        if len(emptyShelf) > 0:
            for i in range(len(emptyShelf)):
                try:
                    goalState.append(restack.ON(emptyShelf[i+1], emptyShelf[i]))
                except IndexError:
                    continue
            goalState.append(restack.ONTABLE(emptyShelf[0]))
            goalState.append(restack.TOPBOTTLE(emptyShelf[-1]))
        
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
    onstand.delivered()
    onstand.setCurVolume(0)
    onstand.empty()
    bottles = []
    for i in range(3):
        bottles.append(Bottle())
    [b.delivered() for b in bottles]    
    [print(b) for b in bottles]
    
    emptyBottle = Bottle()
    emptyBottle.setCurVolume(0)
    
    robot = Robot()
    robot.restack(bottles, onstand, [emptyBottle])
    
    

