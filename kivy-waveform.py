from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

import librosa


class WaveformWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data, self.sr = librosa.load('cover.wav',sr=44100)
        self.draw_waveform()

    def draw_waveform(self):
        with self.canvas:
            Color(1, 1, 1)  # Set the color to white
            height = self.height / 2
            data_len = len(self.data)
            for i in range(0,data_len - 1,self.sr):
                x1 = i / data_len * self.width
                y1 = height + self.data[i] * height
                x2 = (i + 1) / data_len * self.width
                y2 = height + self.data[i + 1] * height
                Line(points=[x1, y1, x2, y2], width=1)
            print("END",x1,y1,x2,y2,self.width,self.height)


class WaveformApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        
        waveform = WaveformWidget(self)
        self.window.add_widget(waveform)
        return self.window


if __name__ == '__main__':
    WaveformApp().run()