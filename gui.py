import itertools
import random
import string

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

import aips
import simulation
from graph import Graph,Node, Edge

kivy.require("2.1.0")
SIMULATION = simulation.Simulation()

class NumCustomersWindow(Screen):
    #first window
    #asks user for number of customers
    numCustomers = ObjectProperty(None)
    
    def submit(self):
        if self.numCustomers.text != "":
            try:
                num = int(self.numCustomers.text)
                global SIMULATION
                SIMULATION = simulation.Simulation(num)
                self.reset()
                sm.current = "name"
            except:
                invalidForm()
        else:
            invalidForm()
            
    def reset(self):
        self.numCustomers.text = ""

class NameWindow(Screen):
    #second window
    #asks user for the name of customers
    names = ObjectProperty(None)
    def on_enter(self, *args):
        body = self.ids.body
        #self.add_widget(Label(text="Hello"))
        #self.ids.body.add_widget(Label(text="Hello"))
        global SIMULATION
        print(SIMULATION.numCustomers)
        self.nameInput = []
        for i in range(SIMULATION.numCustomers):
            self.ids.body.add_widget(Label(text=f"Name of customer {i+1}",
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.5,0.12),
                pos_hint={"x":0,"top":0.8 - i*0.13}
                
                                     
            ))
            #width,height = Window.size
            self.nameInput.append(TextInput(  
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.4,0.12),
                pos_hint={"x":0.5,"top":0.8 - i*0.13},
                multiline=False))
            self.ids.body.add_widget(self.nameInput[i])
    
    def submit(self):
        successful = True
        global SIMULATION
        for w in self.nameInput:
            if w.text != "":
                
                c = aips.Customer(w.text)
                SIMULATION.add_customer(c)
            else:
                successful = False
                invalidForm()
        if successful:
            print(SIMULATION.customers)
            self.reset()
            sm.current = "distance"
                
    def reset(self):
        for w in self.nameInput:
            w.text = ""

class DistanceWindow(Screen):
    #third window
    #asks user for the distances of the customers
    
    def on_enter(self, *args):
        global SIMULATION
        numComb = itertools.combinations(SIMULATION.customers,2)
        self.distInput = []
        for i in range(len(SIMULATION.customers)):
            self.ids.body.add_widget(Label(text=f"Distance between {SIMULATION.customers[i]} and {SIMULATION.dispatcher}",
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.5,0.12),
                pos_hint={"x":0,"top":0.8 - i*0.13}
            ))
            #width,height = Window.size
            self.distInput.append(TextInput(  
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.4,0.12),
                pos_hint={"x":0.5,"top":0.8 - i*0.13},
                multiline=False))
            self.ids.body.add_widget(self.distInput[i])
            
        for c in list(numComb):
            cust1 = c[0]
            cust2 = c[1]
            self.ids.body.add_widget(Label(text=f"Distance between {cust1} and {cust2}",
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.5,0.12),
                pos_hint={"x":0,"top":0.8 - i*0.13}
            ))
            #width,height = Window.size
            self.distInput.append(TextInput(  
                font_size=(self.width**2 + self.height**2) / 14**4,
                size_hint=(0.4,0.12),
                pos_hint={"x":0.5,"top":0.8 - i*0.13},
                multiline=False))
            self.ids.body.add_widget(self.distInput[SIMULATION.numCustomers +i])
        

class SimWindow(Screen):
    #fourth window
    #main window
    #where the simulation will run
    pass
        
class WindowManager(ScreenManager):
    pass



def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

        
kv = Builder.load_file("AID.kv")

sm = WindowManager()

screens = [NumCustomersWindow(name="number"), 
           NameWindow(name="name"), 
           DistanceWindow(name="distance"),
           SimWindow(name="simulation")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "number"

class AIDApp(App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    AIDApp().run()