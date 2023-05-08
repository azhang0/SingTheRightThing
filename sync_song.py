from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
from kivy_garden.graph import Graph, MeshLinePlot
from audio_modality import *

from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from math import sin
from kivy.uix.label import Label


hop_size = 2205
sr = 22050
# https://librosa.org/librosa_gallery/auto_examples/plot_music_sync.html
def parse_sounds(path1,path2):
    '''
    Parses and plots the sound waves of the files at path
    '''
    x_1, fs1 = librosa.load(path1)
    x_2, fs2 = librosa.load(path2)
    return x_1,x_2

def extract_chroma(path1,path2):
    '''
    Extracts chroma features of the two songs
    '''
    x_1,x_2 = parse_sounds(path1,path2)
    n_fft = 4410
    x_1_chroma = librosa.feature.chroma_stft(y=x_1, tuning=0, norm=2,
                                            hop_length=hop_size, n_fft=n_fft)
    x_2_chroma = librosa.feature.chroma_stft(y=x_2, tuning=0, norm=2,
                                            hop_length=hop_size, n_fft=n_fft)

    return x_1_chroma,x_2_chroma

def align_chroma(path1,path2):
    '''
    Aligns timestamps
    '''
    x_1_chroma,x_2_chroma = extract_chroma(path1,path2)
    swap = False #based off length
    if np.shape(x_2_chroma)[1]<np.shape(x_1_chroma)[1]:
        swap = True
        temp = x_1_chroma
        x_1_chroma = x_2_chroma
        x_2_chroma = temp
    
    D, wp = librosa.sequence.dtw(X=x_1_chroma, Y=x_2_chroma, metric='euclidean')
    
    wp = wp[::-1] #sort by earliest start
    if swap:
        wp = [[a[1],a[0]] for a in wp] 
    wp = np.asarray(wp)
    wp_s = wp * hop_size / sr #convert to seconds
    return wp_s,wp

def plot_correspondences_matplotlib(path1,path2,wp):
    x_1,x_2 = parse_sounds(path1,path2)
    fig = plt.figure(figsize=(16, 8))
    # Plot x_1
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(x_1)
    plt.title('Original')
    ax1 = plt.gca()
    print("X1")
    # Plot x_2
    plt.subplot(2, 1, 2)
    librosa.display.waveplot(x_2)
    plt.title('Yours')
    ax2 = plt.gca()
    print("X2")


    plt.tight_layout()

    trans_figure = fig.transFigure.inverted()
    lines = []
    arrows = 30
    points_idx = np.int16(np.round(np.linspace(0, wp.shape[0] - 1, arrows)))

    # for tp1, tp2 in zip((wp[points_idx, 0]) * hop_size, (wp[points_idx, 1]) * hop_size):
    for tp1, tp2 in wp[points_idx] * hop_size / sr:
        # get position on axis for a given index-pair
        coord1 = trans_figure.transform(ax1.transData.transform([tp1, 0]))
        coord2 = trans_figure.transform(ax2.transData.transform([tp2, 0]))

        # draw a line
        line = matplotlib.lines.Line2D((coord1[0], coord2[0]),
                                    (coord1[1], coord2[1]),
                                    transform=fig.transFigure,
                                    color='r')
        lines.append(line)
    print("LINES")
    fig.lines = lines
    plt.tight_layout()
    plot_path = 'plots/correspondences.png'
    plt.savefig(plot_path)
    return plot_path

def plot_correspondences(path1, path2, wp_s):
    x_1, x_2 = parse_sounds(path1, path2)
    max_x = max(len(x_1),len(x_2))//sr
    min_y = 2*float(min(min(x_1),min(x_2)))
    max_y = 2*float(max(max(x_1),max(x_2)))

    graph = Graph(xlabel='Time (s)', ylabel='Amplitude',x_grid_label=True,
                  padding=5, x_ticks_major=5,xlog=False, ylog=False, x_grid=True, y_grid=True,ymin=min_y,ymax=max_y,xmax=max_x)

    plot1 = MeshLinePlot(color=[1, 1, 1, 1]) 
    plot2 = MeshLinePlot(color=[1, 1, 1, 1])

    # Add data to the plots
    plot1.points = [(i/sr, 1+x_1[i]) for i in range(0,len(x_1),sr)]
    plot2.points = [(i/sr, x_2[i]-1) for i in range(0,len(x_2),sr)]
    graph.add_plot(plot1)
    graph.add_plot(plot2)

    # # Add lines connecting corresponding points
    arrows = 30
    points_idx = np.int16(np.round(np.linspace(0, wp_s.shape[0], arrows+1)))[:-1]
    
    for tp1, tp2 in wp_s[points_idx]:
        plot1_point = plot1.points[int(tp1)]
        plot2_point = plot2.points[int(tp2)]
        plot_color = [1, 0, 0, 1]
        plot = MeshLinePlot(color=plot_color)#, width=2)

        plot.points = [plot1_point, plot2_point]
        graph.add_plot(plot)
    return graph

if __name__ == "__main__":
    orig,cover = 'orig.wav','cover.wav'
    wp = align_chroma(orig,cover)[1]
    graph = plot_correspondences(orig,cover,wp)
    dictate('time to plot')
    class SayHello(App):
        def build(self):
            #returns a window object with all it's widgets
            self.window = GridLayout()
            self.window.cols = 1
            self.window.size_hint = (0.9, 0.7)
            self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
            
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
    SayHello().run()
    
    dictate('DONE')

