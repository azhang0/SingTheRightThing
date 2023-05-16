
from parse_song import *
from sync_song import *
from calc_score import *
from audio_modality import *

def try_this():
    demo_response = start_up()
    orig,cover = select_song(demo_response),select_cover(demo_response)
    orig,cover = extract_vocals(orig,cover)        
    analyze(orig,cover)

def start_up():
    welcome_text = "Welcome to SingTheRightThing, where you can receive feedback on your singing performance!"
    dictate(welcome_text)
    demo_selection = "Do you want to see a demo, first? Speak after the beep."
    dictate(demo_selection)
    demo_response = record_and_transcribe(query=demo_selection)
    return demo_response
   
def select_song(demo=False,orig='orig.wav'):
    if demo:
        demo_intro = "Awesome! The demo song is Taylor Swift's 'Blank Space'."
        dictate(demo_intro)  
    else:
        song_selection = "What is the name of the song you will be singing today?"
        dictate(song_selection)
        song_name = record_and_transcribe(query=song_selection)
        artist_selection = f"Who is the artist of '{song_name}'?"
        dictate(artist_selection)
        song_artist = record_and_transcribe(query=artist_selection)
        song_search = f"Insert the URL for {song_name} by {song_artist}"
        dictate(song_search)
        orig_link = input(song_search)
        dictate(f'Downloading {song_name} by {song_artist}...')
        orig = youtube2wav(orig_link,'new_orig.wav')
    dictate(f'Finished downloading. Here are the first 10 seconds: ')
    play_sound(orig,duration=10)
    move_on = True
    if not demo:
        next_step = "Is this what you were looking for? Say 'YES' to continue, 'NO' to start over with song selection."
        move_on = record_and_transcribe(next_step,bool=True)
    if not demo or move_on:
        return orig
    else:
        dictate('Trying again.')
        select_song()

def select_cover(demo=False,cover='cover.wav'):
    if not demo:
        record_selection = "If you already have a recording of your singing, insert the path to that file. Otherwise, press enter to record live."
        dictate(record_selection)
        cover = input(record_selection)
        if cover is None:
            cover = record_and_save('new_cover.wav')
    dictate('Here are the first 10 seconds of your cover: ')
    play_sound(cover,duration=10)
    return cover
   
def extract_vocals(orig,cover):
    description = 'To allow for more accurate results, I will extract the vocal portions of the original song and your cover. '
    dictate(description) 
    orig = voice_only(orig)
    dictate('Here are the first 10 seconds of the original song.')
    play_sound(orig,10)
    cover = voice_only(cover)
    dictate('Here are the first 10 seconds of the cover.')
    play_sound(cover,10)
    return orig,cover

def analyze(orig,cover):
    orig_notes,cover_notes = wav2notes(orig),wav2notes(cover)

    dictate('I will now use signal processing to map corresponding points in your performance with the original')
    wp_s,wp = align_chroma(orig,cover,True)
    dictate('I will now calculate your score')
    score,points1,points2,most_diff = calc_2(wp,orig_notes,cover_notes)
    print(f"\n\nGreat job! Your score is {score}. See the plot for practice suggestions.")

if __name__=="__main__":
    try_this()



    






