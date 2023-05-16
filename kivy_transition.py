from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from parse_song import *
from sync_song import *
from calc_score import *
from audio_modality import *
from matplotlib import pyplot as plt
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import time

button_press = Animation(background_color=[0, 0, 1, 1], duration=0.5) + \
               Animation(background_color=[1, 1, 1, 1], duration=0.5)


def control_menu(screen,prev=True,music=False,two_types=False):
    command = record_and_transcribe(timeout=None,beep=False)
    if command=='next':
        if music:
            screen.sound.stop()   
        button_press.start(screen.ids.next)
        screen.ids.next.dispatch('on_release')
        return
    if prev:
        if command=='previous':
            if music:
                screen.sound.stop() 
            button_press.start(screen.ids.previous)
            screen.ids.previous.dispatch('on_release')
            return
    if two_types:
        if 'original' in command:
            if not screen.original_toggle:
                screen.sound.stop()
                screen.ids.cover.background_color = [1,1,1,1]
                screen.ids.original.background_color = [0,0,1,1]
                screen.ids.original.dispatch('on_release')
                screen.original_toggle = True
                screen.sound = SoundLoader.load(screen.manager.orig_vocals_path)
        elif 'cover' in command:
            if screen.original_toggle:
                screen.sound.stop()
                screen.ids.original.background_color = [1,1,1,1]
                screen.ids.cover.background_color= [0,0,1,1]
                screen.ids.cover.dispatch('on_release')
                screen.original_toggle = False
                screen.sound = SoundLoader.load(screen.manager.cover_vocals_path)
        elif 'full song' in command:
            if not screen.full_toggle:
                screen.sound.stop()
                screen.sound = SoundLoader.load(screen.manager.cover_vocals_path)
                screen.ids.snippet.background_color = [1,1,1,1]
                screen.ids.full.background_color = [0,0,1,1]
                screen.ids.full.dispatch('on_release')
                screen.full_toggle = True
        elif 'red part' in command:
            if  screen.full_toggle:
                screen.sound.stop()
                screen.sound = SoundLoader.load(screen.manager.cover_vocals_path)
                screen.sound.seek(screen.most_diff)
                Clock.schedule_once(screen.sound.stop(), 10)
                screen.ids.full.background_color = [1,1,1,1]
                screen.ids.snippet.background_color = [0,0,1,1]
                screen.ids.snippet.dispatch('on_release')
                screen.full_toggle = False
        else:
            dictate('Invalid prompt given. Please try again.')        
    if music:
        if 'play' in command:
            if screen.manager.orig_path is not None:
                screen.ids.play.dispatch('on_release')
                screen.sound.play()
            else:
                dictate('No song loaded.')
        elif 'pause' in command:
            if screen.manager.orig_path is not None:
                screen.ids.pause.dispatch('on_release')
                screen.sound.stop()   
            else:
                dictate('No song loaded.')
        else:
            dictate('Invalid prompt given. Please try again.')
    else:
        dictate('Invalid prompt given. Please try again.')
    control_menu(screen,prev,music,two_types)

    
class MainWindow(Screen):
    welcome_text =  'Welcome to SingTheRightThing, where you can receive feedback on your pitch and timing to become a better singer today!'
    # welcome_text = 'skip'
    def start_app(self):
        dictate(self.welcome_text)

class SecondWindow(Screen): #demo
    demo_query = 'Would you like to hear a demo first? Speak after the tone.'
    def on_enter(self):
        self.demo_selection()

    def demo_selection(self):
        self.manager.demo = record_and_transcribe(self.demo_query,bool=True,timeout=None)
        if self.manager.demo:
            # button_press.start(self.ids.yes)
            # time.sleep(5) 
            self.ids.yes.dispatch('on_release')
        else:
            # button_press.start(self.ids.no)
            # time.sleep(0.5)
            self.ids.no.dispatch('on_release')

        
class ThirdWindow(Screen): #song
    song_query = 'What is the title of the song?'
    artist_query = 'Who is the artist?'
    def on_enter(self):
        self.song_selection()

    def song_selection(self):
        self.manager.song = record_and_transcribe(self.song_query)
        self.manager.artist = record_and_transcribe(self.artist_query) 
        dictate(f'You chose {self.manager.song} by {self.manager.artist}. Please type in the link to the youtube audio. When you are done, press the submit button.')
    
    def process_link(self):
        yt_url = self.ids.yt_url.text
        self.manager.orig_path = youtube2wav(yt_url,'new_orig.wav') #To-do
        self.sound = SoundLoader.load(self.manager.orig_path)
        dictate('Finished downloading.')
        control_menu(self,prev=True,music=True)

class ThirdWindowDemo(Screen): #song
    def on_enter(self):
        self.song_selection()
        control_menu(self,prev=True,music=True)
   
    def song_selection(self):
        self.manager.song = 'Blank Space'
        self.manager.artist = 'Taylor Swift'
        self.manager.orig_path = 'orig.wav'
        dictate(f'The demo song is {self.manager.song} by {self.manager.artist}')       
        self.sound = SoundLoader.load(self.manager.orig_path)
    

class FourthWindow(Screen): #cover
    record_cover_query = 'When you are ready, click record to record your cover.'
    def on_enter(self):
        dictate(self.record_cover_query)

    def record_cover(self):
        self.manager.cover_path = record_and_save('new_cover.wav')
        self.sound = SoundLoader.load(self.manager.cover_path)
        dictate('finished downloading cover')
        control_menu(self,prev=True,music=True)


class FourthWindowDemo(Screen): #cover
    def on_enter(self):
        self.cover_selection()
        control_menu(self,prev=True,music=True)

    def cover_selection(self):
        self.manager.cover_path = 'cover.wav'
        dictate("The demo cover is from Ali Brustofski's YouTube channel.")
        self.sound = SoundLoader.load(self.manager.cover_path)        


class FifthWindow(Screen): #strip audio
    original_toggle = True
    explanation = 'To allow for more accurate results, I will extract the vocal portions \nof the original song and your cover. This may take a few seconds.'

    def on_enter(self):
        self.strip_audio()
        control_menu(self,music=True,two_types=True)

    def strip_audio(self):
        dictate(self.explanation)
        self.manager.orig_vocals_path = voice_only(self.manager.orig_path)
        self.manager.cover_vocals_path = voice_only(self.manager.cover_path)
        dictate('Done extracting vocals.')
        self.sound = SoundLoader.load(self.manager.orig_vocals_path)


class FakeSixthWindow(Screen): #correspondence transition
    explanation = 'I will now use signal processing to map corresponding points \nin your performance with the original. This will also take a few seconds.'
    def on_enter(self):
        self.find_correspondences()

    def find_correspondences(self):
        dictate(self.explanation)
        self.manager.wp_s,self.manager.wp = align_chroma(self.manager.orig_vocals_path,self.manager.cover_vocals_path)
        self.manager.synced_graph = plot_correspondences(self.manager.orig_vocals_path,self.manager.cover_vocals_path,self.manager.wp_s)
        dictate('Done mapping correspondences.')
        self.ids.next.dispatch('on_release')
        return

class SixthWindow(Screen): #correspondence
    def on_enter(self):
        control_menu(self)

class FakeSeventhWindow(Screen): #score transition
    full_toggle = True

    def on_enter(self):
        self.do_score()

    def do_score(self): 
        dictate('I will now calculate your score')
        orig_notes,cover_notes = wav2notes(self.manager.orig_vocals_path),wav2notes(self.manager.cover_vocals_path)
        score,points1,points2,self.most_diff = calc_2(self.manager.wp,orig_notes,cover_notes)
        caption = f'Your accuracy score is {score}. Good job!\nTry working on the section from {format_seconds(self.most_diff,None)} to {format_seconds(self.most_diff+10,None)} (highlighted in red).'
        dictate(caption)
        self.manager.score_graph = plot_pitch(score,points1,points2,self.most_diff)
        self.ids.next.dispatch('on_release')
        # self.add_widget(self.manager.score_graph)


class SeventhWindow(Screen): #score
    full_toggle = True

    def on_enter(self):
        control_menu(self,two_types=True)

   
class EighthWindow(Screen): #playback
    pass


class WindowManager(ScreenManager):
    demo = None
    orig_path = None
    cover_path = None
    orig_vocals_path = None
    cover_vocals_path = None
    synced_path = None
    synced_graph = None
    score_graph = None




kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
