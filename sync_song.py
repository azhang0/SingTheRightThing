from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display

hop_size = 2205
sr = 22050
# https://librosa.org/librosa_gallery/auto_examples/plot_music_sync.html
def parse_sounds(path1,path2):
    '''
    Parses and plots the sound waves of the files at path
    '''
    x_1, fs1 = librosa.load(path1)
    x_2, fs2 = librosa.load(path2)
    # max_dur = max(len(x_1),len(x_2))
    # # plt.figure("Waveplots",figsize=(16, 8))
    # fig,(ax1,ax2) = plt.subplots(2,1)
    # fig.suptitle('Waveplots')
    # # plt.subplot(2, 1, 1)
    # ax1.set_title("Original")
    # ax1.set_xlim([0,max_dur])
    # # plt.figure("Waveplot for " + path1,figsize=(16, 8))
    # librosa.display.waveplot(x_1,ax=ax1)

    # # plt.subplot(2, 1, 2)
    # ax2.set_title("Yours")
    # ax2.set_xlim([0,max_dur])


    # # plt.figure("Waveplot for " + path2,figsize=(16, 8))
    # librosa.display.waveplot(x_2,ax=ax2)
    # plot_path = 'plots/waveforms.png'
    # plt.savefig(plot_path)
    return x_1,x_2

def extract_chroma(path1,path2):
    '''
    Extracts chroma features of the two songs
    '''
    x_1,x_2 = parse_sounds(path1,path2)
    n_fft = 4410
    hop_size = 2205

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
    wp_s = np.asarray(wp) * hop_size / sr #convert to seconds
    return wp_s,wp

def plot_correspondences(path1,path2,wp):
    x_1,x_2 = parse_sounds(path1,path2)
    print("PARSED")
    fig = plt.figure(figsize=(16, 8))
    print("FIG CREATED")
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

    
if __name__ == "__main__":
    orig,cover = 'orig.wav','cover.wav'
    parse_sounds(orig,cover)
    plot_correspondences(orig,cover)

