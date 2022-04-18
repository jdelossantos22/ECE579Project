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
SIMULAION = simulation.Simulation()

class NumCustomersWindow(Screen):
    #first window
    #asks user for number of customers
    numCustomers = ObjectProperty(None)
    
    def submit(self):
        if self.numCustomers.text != "":
            try:
                num = int(self.numCustomers.text)
                SIMULAION = simulation.Simulation(num)
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
        self.ids.body.add_widget(Label(text="Hello"))
        
        for i in range(SIMULAION.numCustomers):
            self.ids.body.add_widget(Label(text="Hello2"))
            width,height = Window.size
            self.nameInput = TextInput(  
                font_size=42,
                multiline=False)
            self.ids.body.add_widget(self.nameInput)
        pass

class DistanceWindow(Screen):
    #third window
    #asks user for the distances of the customers
    
    pass

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