from pytube import YouTube
from moviepy.editor import *
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from spleeter.separator import Separator
import soundfile as sf
# import ffmpeg
from basic_pitch.inference import predict

def youtube2wav(link,name='orig'):
    '''
    Takes in YouTube URL and outputs a WAV file
    '''
    yt = YouTube(link,use_oauth=True,allow_oauth_cache=True)
    # yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    destination = '.'
    out_file = video.download(output_path=destination)
    mp3_file = 'orig' + '.mp3'
    os.rename(out_file, mp3_file)
    audio = AudioFileClip(mp3_file)
    audio.write_audiofile(f"{name}.wav")  
    print(yt.title + " has been successfully downloaded.")
    os.remove(mp3_file)
    return f"{name}.wav"

def voice_only(orig_file,new_dir='.'):
    '''
    Extracts vocals from orig file, returns path of new file
    '''
    separator = Separator('spleeter:2stems',multiprocess=False)
    separator.separate_to_file(orig_file,new_dir)
    name = orig_file.split(".")[0]
    return new_dir+'/'+name+'/'+'vocals.wav'


def wav2notes(path):
    '''
    Uses basic pitch api to predict midi
    '''
    notes = predict(path)[2]
    notes = sorted(notes,key = lambda a:a[0]) #sort by start
    return notes

if __name__ == "__main__":
    print("here")
    n = voice_only('orig.wav')
    print(n)
    # yt = 'https://www.youtube.com/watch?v=HVlSWs8-LjU&pp=ygUYYmxhbmsgc3BhY2UgdGF5bG9yIHN3aWZ0'
    # youtube2wav(yt)
    # new_song = voice_only('cover.wav','test')
    # print(new_song)



