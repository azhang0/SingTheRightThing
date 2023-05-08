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
from sync_song import *
from kivy import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
import librosa
from calc_score import *
Config.set('graphics', 'gles_version', '3.0')
Config.write()

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

class MyVersion(App): #correspondences
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        wp_s,wp = align_chroma('orig.wav','cover.wav')
        graph = plot_correspondences('orig.wav','cover.wav',wp_s)
        self.window.add_widget(graph)
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

class MyScore(App): #correspondences
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        wp_s,wp = align_chroma('orig.wav','cover.wav')
        orig_notes,cover_notes = wav2notes('orig.wav'),wav2notes('cover.wav')
        score,points1,points2,most_diff = calc_2(wp,orig_notes,cover_notes)
        ##
        graph = plot_pitch(score,points1,points2,most_diff)
        
        self.window.add_widget(graph)

        # label widget
        self.greeting = Label(
                        text= "What's your name?",
                        font_size= 16,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)
        #graph widget
        return self.window


# run Say Hello App Calss
if __name__ == "__main__":
    MyScore().run()
    # dictate('DONE')
    # SayHello().run()
    # WaveformApp().run()
    
    