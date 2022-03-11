import itertools
class Shelf:
    def __init__(self):
        return
    
class Stand:
    def __init__(self):
        return

class Chilled_Stand:
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
        