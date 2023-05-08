from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from audio_modality import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from kivy_garden.graph import Graph, MeshLinePlot
from math import sin


# Audio loads after
class SayHello(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=25, y_ticks_major=1,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        self.window.add_widget(graph)
        print("HERE",graph.size)
        graph.export_to_png('plots/pls.png')

        # label widget
        self.greeting = Label(
                        text= "What's your name?",
                        font_size= 16,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        

        #graph widget
        return self.window
    #     self.built = False

    # def build(self):
    #     self.built = True
    #     self.on_enter()
    #     welcome_text =  'Welcome to SingTheRightThing, where you can receive feedback on your pitch and timing to become a better singer today! Before we get started, what is your name?'
    #     dictate(welcome_text)
    #     matplotlib.use("TkAgg")

    #     print("HELLO",matplotlib.get_backend())

    #     fig = plt.figure(figsize=(16, 8))

    #     name = record_and_transcribe(welcome_text,timeout=5)
    #     # dictate(f'Hello {name}!')
    #     # name = 'dick'
    #     self.greeting.text = "Hello " + name + "!\n"
    #     dictate(self.greeting.text)

    #     return self.window
    
    # def on_enter(self):
    #     return


# run Say Hello App Calss
if __name__ == "__main__":
    SayHello().run()
    