from youtube_transcript_api import YouTubeTranscriptApi

from gensim.summarization import keywords

from moviepy.editor import *

from pytube import YouTube

import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import find_peaks

def generate_id(Link):
    text = Link.split('=')
    id = text[1]
    return id

def srt_generation(id):
    srt = YouTubeTranscriptApi.get_transcript(id)
    return srt

def get_link(Link):
    id = generate_id(Link)
    # yt = YouTube(Link)
    # yt.streams.filter(progressive=True, file_extension='mp4').download('static/Input/Link.mp4')
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
    # print(type(keyphrases))
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
    counter = 1
    clip = VideoFileClip("static/Input/Link.mp4")
    for row in range(len(trimmed_data)):
        print("Creating subclip: {} ".format(counter))
        ###############################################################################################################

                                                        # OUTPUT FILE NAME AND TRIMMING

        ###############################################################################################################
        outputName = 'static/Output/output_'+ str(counter) + '.mp4'
        outputAudio = 'static/Audio/output_' + str(counter) + '.mp3'
        # ouputGraph = 'static/Graph/output_' + str(counter) + '.png'
        startTime = trimmed_data[row]['start']
        endTime = trimmed_data[row]['endtime']
        # print(row)
        subclip_ = clip.subclip(startTime, endTime)
        ###############################################################################################################

                                                        # VIDEO PROCESSING

        ###############################################################################################################
        subclip_.write_videofile(outputName)
        ###############################################################################################################

                                                        # AUDIO PROCESSING

        ###############################################################################################################
        subclip_.audio.write_audiofile(outputAudio)
        ###############################################################################################################

                                                        # CREATING GRAPHS

        ###############################################################################################################
        # wav_obj = subclip_.audio
        # sample_freq = wav_obj.getframerate()
        # n_samples = wav_obj.getnframes()
        # t_audio = n_samples/sample_freq
        # n_channels = wav_obj.getnchannels()
        # signal_wave = wav_obj.readframes(n_samples)
        # signal_array = np.frombuffer(signal_wave, dtype=np.int16)
        # l_channel = signal_array[0::2]
        # r_channel = signal_array[1::2]
        # times = np.linspace(0, n_samples/sample_freq, num=n_samples)
        # plt.figure()
        # plt.plot(times, l_channel)
        # plt.title('Left Channel')
        # plt.ylabel('Signal Value')
        # plt.xlabel('Time (s)')
        # plt.xlim(0, t_audio)
        # plt.savefig(ouputGraph, dpi = 300)
        trimmed_data[row]['filepath'] = outputName
        trimmed_data[row]['audiopath'] = outputAudio
        # trimmed_data[row]['graphpath'] = ouputGraph

        counter += 1
    print(trimmed_data)


    return trimmed_data