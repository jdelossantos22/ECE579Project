import itertools
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import aips

kivy.require("2.1.0")

class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super(ConnectPage, self).__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text="Please enter the number of customers for simulation: "))
        self.customers = TextInput(multiline=False, input_filter="int")
        self.add_widget(self.customers)
        
        self.submit = Button(text="Submit", font_size=32)
        self.submit.bind(on_press=self.initiate_sim)
        self.empty = Label()
        self.add_widget(self.empty)
        self.add_widget(self.submit)
    
    def initiate_sim(self, instance):
        self.numCustomers = int(self.customers.text)
        self.custNames = []
        self.remove_widget(self.empty)
        self.remove_widget(self.submit)
        #name of customers
        for i in range(self.numCustomers):
            self.add_widget(Label(text=f"Please enter name for customer {i}: "))
            self.custNames.append(TextInput(multiline=False))
            self.add_widget(self.custNames[i])
            
        #new submit button
        self.submit.bind(on_press=self.ask_distance)
        self.add_widget(self.submit)
        
    def ask_distances(self, instance):
        #remove buttons for now
        self.remove_widget(self.empty)
        self.remove_widget(self.submit)
        
        numComb = itertools.combinations(self.customers,2)
        #ask for distance between customers and 
        for i in range(self.numCustomers):
            pass
    def run_sim(self, instance):
        pass

class AIDApp(App):
    def build(self):
        return ConnectPage()

if __name__ == "__main__":
    AIDApp().run()
    