import itertools
import random
import string
from turtle import window_height

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import aips
from graph import Graph,Node, Edge

kivy.require("2.1.0")

class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.cols = 1
        self.top_grid = GridLayout()
        self.top_grid.cols = 2
        
        
        self.top_grid.add_widget(Label(text="Please enter the number of customers for simulation: "))
        
        self.wNumCustomers = TextInput(multiline=False, input_filter="int")
        self.top_grid.add_widget(self.wNumCustomers)
        
        #add top grid
        self.add_widget(self.top_grid)
        
        self.wSubmit = Button(text="Submit", 
            font_size=32,
            size_hint_y=None,
            height=100)
        
        self.wSubmit.bind(on_press=self.process_submit)
        #self.wEmpty = Label()
        #self.add_widget(self.wEmpty)
        self.add_widget(self.wSubmit)
    
    def process_submit(self, instance):
        pass
    
    def initiate_sim(self, instance):
        self.numCustomers = int(self.wNumCustomers.text)
        self.wCustNames = []
        
        #self.clear_widgets()#clear widgets/screen
        
        #name of customers
        for i in range(self.numCustomers):
            self.top_grid.add_widget(Label(text=f"Please enter name for customer {i}: "))
            self.wCustNames.append(TextInput(multiline=False))
            self.top_grid.add_widget(self.wCustNames[i])
            
        #new submit button
        self.wSubmit.bind(on_press=self.ask_distances)
        self.top_grid.add_widget(self.wSubmit)
    
    
    
    def ask_distances(self, instance):
        #remove buttons for now
        self.process_customers()
        self.clear_widgets()
        
        
        numComb = itertools.combinations(self.customers,2)
        self.wDistance = []
        #ask for distance between customers and 
        for i in range(len(self.customers)):
            self.add_widget(Label(text=f"Please enter distance between {str(self.customers[i])} and {str(self.dispatcher)}: "))
            self.wDistance.append(TextInput(multiline=False, input_filter="float"))
            self.add_widget(self.wDistance[i])
            
        for c in list(numComb):
            cust1 = c[0]
            cust2 = c[1]
            self.add_widget(Label(text=f"Please enter distance between {str(cust1)} and {str(cust2)}: "))
            self.wDistance.append(TextInput(multiline=False, input_filter="float"))
            self.add_widget(self.wDistance[i])
        
        #new submit button
        self.wSubmit.bind(on_press=self.process_distances)
        self.add_widget(self.wSubmit)
            
        
    def process_customers(self):#instantiate Customers
        self.dispatcher = aips.Dispatcher()
        self.customers = []
        self.graph = Graph()
        self.graph.add_node(self.dispatcher)
        for w in self.wCustNames:
            name = w.text
            if name == "":
                name = random.choice(string.ascii_letters)
            c = aips.Customer(name)
            self.customers.append(c)
            self.graph.add_node(c)
            
    def process_distances(self, instance):
        for i in range(len(self.wDistance)):
            dist = float(self.wDistance[i].text)
            dist = random.uniform(1, 50) if dist == "" else dist
            if i < self.numCustomers:
                self.graph.add_edge(self.dispatcher,self.customers[i],float(dist))
            else:
                pass
            
        pass
            
    def run_sim(self, instance):
        pass

class AIDApp(App):
    def build(self):
        return MainPage()

if __name__ == "__main__":
    AIDApp().run()
'''
global G
        val_map = {'A': 1.0,
                   'D': 0.5714285714285714,
                              'H': 0.0}
        values = [val_map.get(node, 0.45) for node in G.nodes()]
        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
        red_edges = []
        edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
        pos=nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        nx.draw(G,pos, node_color = values, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
        
        box = self.ids.body
        box.add_widget()
        '''