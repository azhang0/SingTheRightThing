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


# Audio loads after
class SayHello(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.greeting = Label(
                        text= "What's your name?",
                        font_size= 16,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        plt.figure()

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
    