from youtube_transcript_api import YouTubeTranscriptApi

from gensim.summarization import keywords

from moviepy.editor import *

from pytube import YouTube

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
    print(type(keyphrases))
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
        outputName = 'static/Output/output_'+ str(counter) + '.mp4'
        startTime = trimmed_data[row]['start']
        endTime = trimmed_data[row]['endtime']
        print(row)
        subclip_ = clip.subclip(startTime, endTime)
        subclip_.write_videofile(outputName)
        trimmed_data[row]['filepath'] = outputName
        counter += 1
    print(trimmed_data)
    # listofpath = []
    # for row in range(len(trimmed_data)):
    #     listofpath.append(trimmed_data[row]['filepath'])
    # clips_ = concatenate_videoclips([VideoFileClip(file) for file in listofpath])
    # final_clip = concatenate_videoclips(clips_)
    # clips_.write_videofile('static/Output/Final.mp4')
    return trimmed_data