# Welcome to SingTheRightThing!
This tool provides specific and actionable feedback on your singing performance, with a mostly hands-free user interface.

## Set-Up Instructions
1. Download or clone this repo
2. Run `pip3 install requirements.txt`
3. Run `python3 kivy_transition.py`
4. Enjoy!

## File Break-Down
The main files are listed below:
- `app_logic.py`: initial version, system interaction via a command line interface [DEPRECATED]
- `audio_modality.py`: record and play back audio
- `calc_score.py`: algorithm to determine user score and areas of improvement
- `kivy_transition.py`,`my.kv`: user interface logc
- `parse_song.py`: convert songs to WAV files, isolate vocals, and extract pitch
- `sync_song.py`: sync songs with DTW
