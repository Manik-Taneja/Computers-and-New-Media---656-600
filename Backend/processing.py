from youtube_transcript_api import YouTubeTranscriptApi

from gensim.summarization import keywords

from moviepy.editor import *

from pytube import YouTube

import numpy as np

import matplotlib.pyplot as plt
import librosa.display

import numpy as np

import pandas as pd

import librosa
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import matplotlib.pyplot as plt
import librosa.display
from scipy import signal
from scipy.io import wavfile

import os
import subprocess
from scipy.io.wavfile import read
# ffmpeg -i input_video.mp4 -b:a 192K -vn output_audio.mp3


def generate_id(Link):
    text = Link.split('=')
    id = text[1]
    return id

def srt_generation(id):
    srt = YouTubeTranscriptApi.get_transcript(id)
    return srt

def get_link(Link):
    id = generate_id(Link)
    srt_data = srt_generation(id)
    indices_pop = []
    for row in range(len(srt_data)):
        if srt_data[row]['text'][0] == '[':
            indices_pop.append(row)
    print(len(srt_data))
    final_data = []
    text_corpus = ""
    for i in range(len(srt_data)):
        if i not in indices_pop:
            final_data.append(srt_data[i])
            text_corpus += " " + srt_data[i]['text']
    print(len(final_data))
    keyphrases = keywords(text_corpus)
    keyphrases = list(keyphrases.split('\n'))
    indices_select = set()
    for word in keyphrases:
        for row in range(len(final_data)):
            if word in final_data[row]['text']:
                indices_select.add(row)
    trimmed_data = []
    for idx in indices_select:
        trimmed_data.append(final_data[idx])    
    print(len(trimmed_data))
    for row in range(len(trimmed_data)):
        trimmed_data[row]['endtime'] = round(trimmed_data[row]['start'] + trimmed_data[row]['duration'],3)
    ###############################################################################################################

                                     # TESTING TRIMMED DATA LIMITING TO 10 LINES

    ###############################################################################################################

    # trimmed_data = trimmed_data[:10]

    ###############################################################################################################

                                        # INPUT PATH - ALREADY DOWNLOADED FILE

    ###############################################################################################################
    counter = 1
    clip = VideoFileClip("static/Input/Link.mp4")

    ###############################################################################################################

                # DEBUG GRAPH STATEMENT TO PRINT GRAPHS, HEAD OVER TO data.html and enable those fields

    ###############################################################################################################
  
    rungraph = 1

    ###############################################################################################################

                                                    # LOOPING OVER TRIMMED DATA

    ###############################################################################################################

    for row in range(len(trimmed_data)):
        print("Creating subclip: {} ".format(counter))
        ###############################################################################################################

                                                        # OUTPUT FILE NAME AND TRIMMING

        ###############################################################################################################
        outputName = 'static/Output/output_'+ str(counter) + '.mp4'
        outputAudio = 'static/Audio/output_' + str(counter) + '.wav'
        outputGraph = 'static/Graph/output_' + str(counter) + '.png'
        startTime = trimmed_data[row]['start']
        endTime = trimmed_data[row]['endtime']
        subclip_ = clip.subclip(startTime, endTime)
        ###############################################################################################################

                                                        # VIDEO PROCESSING

        ###############################################################################################################
        subclip_.write_videofile(outputName)
        ###############################################################################################################

                                                        # AUDIO PROCESSING

        ###############################################################################################################
        # subclip_.audio.write_audiofile(outputAudio)
        try:
            os.remove(outputAudio)
        except:
            pass
        subprocess.call(['ffmpeg', '-i', outputName, '-b:a', '192K', '-vn', outputAudio])
        
        ###############################################################################################################

                                                        # SPECTROGRAM PROCESSING

        ###############################################################################################################
        if rungraph == 1:
            x, sr = librosa.load(outputAudio)
            x = x [:10000]
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            p = librosa.display.waveshow(x, sr=sr)
            fig.savefig(outputGraph)


        # plt.rcParams["figure.figsize"] = [7.50, 3.50]
        # plt.rcParams["figure.autolayout"] = True
        # input_data = read(outputAudio)
        # audio = input_data[1]
        # plt.plot(audio[0:1024])
        # plt.ylabel("Amplitude")
        # plt.xlabel("Time")
        # plt.savefig(outputGraph)
        # sample_rate, samples = wavfile.read(outputAudio)
        # frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
        # print("F: {}".format(frequencies))
        # print("T: {}".format(times))
        # print("S: {}".format(spectrogram))
        # plt.pcolormesh(times, frequencies, spectrogram)
        # plt.imshow(spectrogram)
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.savefig(outputGraph)

        ###############################################################################################################

                                                        # DEFINING PATHS

        ###############################################################################################################

        trimmed_data[row]['filepath'] = outputName
        trimmed_data[row]['audiopath'] = outputAudio
        if rungraph == 1:
            trimmed_data[row]['graphpath'] = outputGraph
        counter += 1
    # print(trimmed_data)


    return trimmed_data