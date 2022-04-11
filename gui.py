import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

kivy.require("2.1.0")

class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text="Please enter the number of customers for simulation: "))
        self.numCustomers = TextInput(multiline=False)
        self.add_widget(self.numCustomers)
        
        self.proceed = Button(text="Proceed")
        self.proceed.bind(on_press=self.initiate_sim)
        self.add_widget(Label())
        self.add_widget(self.proceed)

class EpicApp(App):
    def build(self):
        return ConnectPage()

if __name__ == "__main__":
    EpicApp().run()
    