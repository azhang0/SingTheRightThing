import time
import simpleaudio as sa
import speech_recognition as sr
from gtts import gTTS
import os
import sys
import io
from numpy import random
import wave
import threading
import multiprocessing
from multiprocessing import Process
from contextlib import contextmanager

YES = ["sure","yes","okay","great","good","yeah"]
NO = ["no","nah"]

def play_sound(filename,duration=None):
    '''
    plays WAV file at filename for specified duration
    '''
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    if duration:
        time.sleep(duration)
        play_obj.stop()
    else:
        play_obj.wait_done()


def record_and_save(filename='cover.wav'):
    play_sound('beep.wav')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source,timeout=None)
    audio_bytes = audio.get_wav_data()
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)  # set the number of channels
        f.setsampwidth(2)  # set the sample width (in bytes)
        f.setframerate(44100)  # set the frame rate (samples per second)
        f.writeframes(audio_bytes)  # write the audio data to the file
    return filename

def record_and_transcribe(query="",timeout=5,silence_ok=False,bool=False,beep=True):
    if query:
        dictate(query)
    if beep:
        play_sound('beep.wav')
    # obtain audio from the microphonef
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source,timeout=timeout,phrase_time_limit=2)
        except:
            dictate(f"I'm sorry, I couldn't catch that. Please try again.")
            time.sleep(0.1)
            return record_and_transcribe(query,timeout,silence_ok,bool)
    # recognize speech using Google Speech Recognition
    try:
        transcription = r.recognize_google(audio)
        dictate("You said: " + transcription)
        if bool:
            if transcription in NO:
                transcription = "NO"
            elif transcription in YES:
                transcription = "YES"
            else:
                dictate("Please give a yes or no answer.")
                return record_and_transcribe(query,timeout,silence_ok,bool)

        return transcription=="YES" if bool else transcription
    except:
        if silence_ok:
            return ""
        else:
            dictate(f"I'm sorry, I couldn't catch that. Please try again.")
            time.sleep(0.1)
            return record_and_transcribe(query,timeout,silence_ok,bool,beep)

def dictate(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    audiofile = f"dictation{random.randint(0,100)}.mp3"
    myobj.save(audiofile)
    os.system(f"mpg321 {audiofile}")
    os.remove(audiofile)


if __name__ == "__main__":
    print("Number of cpu : ", multiprocessing.cpu_count())
    record_and_transcribe("who are you?") 
