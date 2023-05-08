from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from kivy_garden.graph import Graph, MeshLinePlot

import scipy
import librosa
import librosa.display
from basic_pitch.inference import predict
from sync_song import *
from parse_song import *

def calc_1(wp,ne1,ne2):
    '''
    takes in correspondence and note events
    outputs diff directly compared to orig
    '''
    eps = 0.01
    diff = []
    i,j = 0,0
    for t1,t2 in wp:
        while i<len(ne1) and ne1[i][0]+eps<t1:
            i += 1
            if i==len(ne1):
                return sum(diff)/len(diff)
        while j<len(ne2) and ne2[j][0]+eps<t2:
            j += 1
            if j==len(ne2):
                return sum(diff)/len(diff)
        start1,end1,pitch1,amplitude1,_ = ne1[i]
        start2,end2,pitch2,amplitude2,_ = ne2[j]
        diff.append(abs(pitch1-pitch2))
    return sum(diff)/len(diff)

def calc_2(wp,ne1,ne2):
    '''
    More of a slope approach (deltapitch/deltatime)
    '''
    eps = 0.1
    diff = []
    time2 = []
    i,j = 0,0
    plot_start1,plot_pitch1,plot_start2,plot_pitch2 = [],[],[],[]
    prev_pitches = None
    for idx,(t1,t2) in enumerate(wp):
        while i<len(ne1) and ne1[i][0]+eps<t1:
            i += 1
            # if i==len(ne1):
            #     points1 = (plot_start1,plot_pitch1)
            #     points2 = (plot_start2,plot_pitch2)
            #     return 100-float(sum(diff)/len(diff)),points1,points2
        
        while j<len(ne2) and ne2[j][0]+eps<t2:
            j += 1
            # if j==len(ne2):
            #     points1 = (plot_start1,plot_pitch1)
            #     points2 = (plot_start2,plot_pitch2)
            #     return 100-float(sum(diff)/len(diff)),points1,points2
        if i==len(ne1) or j==len(ne2):
            break
        start1,end1,pitch1,amplitude1,_ = ne1[i]
        start2,end2,pitch2,amplitude2,_ = ne2[j]
        plot_start1.append(start1)
        plot_pitch1.append(pitch1)
        plot_start2.append(start2)
        plot_pitch2.append(pitch2)
        if prev_pitches is not None:
            diff_pitch1 = abs(pitch1-prev_pitches[0])
            diff_pitch2 = abs(pitch2-prev_pitches[2])
            delta_pitch = abs(diff_pitch1-diff_pitch2)
            diff_time1 = abs(t1-prev_pitches[1])
            diff_time2 = abs(t2-prev_pitches[3])
            delta_time = abs(diff_time1-diff_pitch2)
            diff.append(delta_pitch)
            time2.append(start2)
        prev_pitches = (pitch1,start1,pitch2,start2)
    points1 = (plot_start1,plot_pitch1)
    points2 = (plot_start2,plot_pitch2)
    most_work_needed = calc_most_work(diff,time2)
    score = 100-0.5*float(sum(diff)/len(diff))
    score = round(score*100)/100.0 #round to 2 decimals
    return score,points1,points2,most_work_needed

def calc_most_work(diff,times):
    '''
    Returns the time for which the 10 secs after results in the highest diff
    '''
    most_diff,time_start = 0,0
    for i in range(5,len(diff)-15):
        cur_diff = sum(diff[i:i+10])
        if cur_diff>most_diff:
            most_diff = cur_diff
            time_start = times[i]
    return time_start

def format_seconds(x,pos):
    minutes = int(x / 60)
    seconds = int(x % 60)
    minutes = f'0{minutes}' if minutes<10 else minutes
    seconds = f'0{seconds}' if seconds<10 else seconds
    return f'{minutes}:{seconds}'

def plot_pitch_matplotlib(score,points1,points2,most_work):
    fig,ax = plt.subplots()
    fig.suptitle(f"Pitch: Original vs Yours\nScore: {str(score)}")
    start1,pitch1 = points1
    plt.plot_date(start1,pitch1,'bo',label="Original")
    start2,pitch2 = points2
    plt.plot_date(start2,pitch2,'go',label="Yours")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_seconds))

    caption = f'Your accuracy score is {score}. Good job!\nTry working on the section from {format_seconds(most_work,None)} to {format_seconds(most_work+10,None)} (highlighted in red).'
    print(caption)
    plt.annotate(caption, xy=(0.5, -0.15), xycoords='axes fraction', fontsize=10, ha='center')

    plt.legend()
    plt.axvspan(most_work, most_work+10, alpha=0.3, color='red')
    plot_path = 'plots/final_score.png'
    plt.savefig(plot_path)
    return plot_path

def plot_pitch(score, points1, points2, most_work):
    graph = Graph(xlabel='Time (seconds)', ylabel='Pitch',size=(800,600))
    graph.title = f'Pitch: Original vs Yours\nScore: {str(score)}'
    graph.x_ticks_major = 1
    graph.y_ticks_major = 100

    # Add the original pitch data
    start1, pitch1 = points1
    plot1 = MeshLinePlot(color=[0, 0, 1, 1])
    plot1.points = [(start1[i], pitch1[i]) for i in range(len(start1))]
    graph.add_plot(plot1)

    # Add the user's pitch data
    start2, pitch2 = points2
    plot2 = MeshLinePlot(color=[0, 1, 0, 1])
    plot2.points = [(start2[i], pitch2[i]) for i in range(len(start2))]
    graph.add_plot(plot2)

    # Highlight the section where the user needs to work on improving their accuracy
    highlight_plot = MeshLinePlot(color=[1, 0, 0, 0.3])
    highlight_plot.points = [(most_work, graph.ymin), (most_work, graph.ymax), 
                             (most_work + 10, graph.ymax), (most_work + 10, graph.ymin)]
    graph.add_plot(highlight_plot)

    caption = f'Your accuracy score is {score}. Good job!\nTry working on the section from {format_seconds(most_work, None)} to {format_seconds(most_work+10, None)} (highlighted in red).'
    print(caption)

    # Add the caption as a label at the bottom of the graph
    label = Label(text=caption, font_size=20, halign='center', valign='middle')
    graph.add_widget(label)

    # Save the graph to an image file
    plot_path = 'plots/final_score.png'
    graph.export_to_png(plot_path)

    return plot_path


if __name__ == "__main__":
    orig,cover = './orig/vocals.wav','./cover/vocals.wav'
    wp_s,wp = align_chroma(orig,cover)
    ne1,ne2 = wav2notes(orig),wav2notes(cover)
    score,p1,p2,most_work = calc_2(np.array(wp),ne1,ne2)
    print("Score: ",score)
    plot_pitch(score,p1,p2,most_work)