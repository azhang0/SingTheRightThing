from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from parse_song import *
from sync_song import *
from calc_score import *
from audio_modality import *
from matplotlib import pyplot as plt


class MainWindow(Screen):
    welcome_text =  'Welcome to SingTheRightThing, where you can receive feedback on your pitch and timing to become a better singer today!'
    welcome_text = 'Next'
    def transition(self):
        dictate(self.welcome_text)


class SecondWindow(Screen): #demo
    demo_query = 'Would you like to hear a demo first? Speak after the tone.'
    def demo_selection(self):
        self.manager.demo = record_and_transcribe(self.demo_query,bool=True)
    
class ThirdWindow(Screen): #song
    #TO-DO: FILE LOOK-UP
    song_query = 'What is the title of the song?'
    artist_query = 'Who is the artist?'

    def song_selection(self):
        if self.manager.demo:
            self.manager.song = 'Blank Space'
            self.manager.artist = 'Taylor Swift'
            self.manager.orig_path = 'orig.wav'
        else:
            self.manager.song = record_and_transcribe(self.song_query)
            self.manager.artist = record_and_transcribe(self.artist_query)    
            self.manager.orig_path = None
        dictate(f'The demo song is {self.manager.song} by {self.manager.artist}')

class FourthWindow(Screen): #cover
    cover_query = 'Do you already have a recording of your cover?'
    record_cover_query = 'When you are ready, click record to record your cover.'

    def cover_selection(self):
        if self.manager.demo:
            self.manager.cover_path = 'cover.wav'
            dictate("The demo cover is from Ali Brustofski's YouTube channel.")
        else:
            cover_exists = record_and_transcribe(self.cover_query,bool=True)
            if cover_exists:
                self.manager.cover_path = record_and_transcribe('Spell out the path to your recording')
            else:
                dictate(self.record_cover_query)
                self.manager.cover_path = record_and_save('new_cover.wav')


class FifthWindow(Screen): #strip audio
    
    def strip_audio(self):
        explanation = 'To allow for more accurate results, I will extract the vocal portions of the original song and your cover. This may take a few seconds.'
        dictate(explanation)
        self.manager.orig_vocals_path = voice_only(self.manager.orig_path)
        self.manager.cover_vocals_path = voice_only(self.manager.cover_path)
        dictate('Done extracting vocals.')


class SixthWindow(Screen): #correspondence
    def find_correspondences(self):
        dictate('I will now use signal processing to map corresponding points in your performance with the original')
        wp_s,self.manager.wp = align_chroma(self.manager.orig_vocals_path,self.manager.cover_vocals_path)
        self.manager.synced_path = plot_correspondences(self.manager.orig_vocals_path,self.manager.cover_vocals_path,self.manager.wp)
        dictate('Done mapping correspondences.')

class SeventhWindow(Screen): #score
    def do_score(self):
        dictate('I will now calculate your score')
        orig_notes,cover_notes = wav2notes(self.manager.orig_vocals_path),wav2notes(self.manager.orig_cover_path)
        score,points1,points2,most_diff = calc_2(self.manager.wp,orig_notes,cover_notes)
        caption = f'Your accuracy score is {score}. Good job!\nTry working on the section from {format_seconds(most_work,None)} to {format_seconds(most_work+10,None)} (highlighted in red).'
        dictate(caption)
        self.manager.score_plot_path =  plot_pitch(score,points1,points2,most_diff)

class EighthWindow(Screen): #playback
    pass


class WindowManager(ScreenManager):
    demo = None
    orig_path = None
    cover_path = None
    orig_vocals_path = None
    cover_vocals_path = None
    synced_path = None




kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
