from moviepy.editor import VideoFileClip, concatenate_videoclips
import librosa
from pydub import AudioSegment
import numpy as np
import pandas as pd
import os

class highlight_generation():

    def __init__(self,path,dataset):
        self.dataset = dataset
        self.path = path

    def data_path(self,directory):
        current_dir = self.path
        parent_dir = os.path.dirname(current_dir)
        path = os.path.join(parent_dir , 'data',directory)
        return path

    def load_audio(self):
        print(f"[-] Converting video file into audio file and loading")
        self.original_video = VideoFileClip(os.path.join(self.data_path('input'),self.dataset))
        audio = self.original_video.audio
        audio.write_audiofile( os.path.join(self.data_path('input'),"cricket.wav"), nbytes=4, codec="pcm_s16le")
        self.x, self.sr = librosa.load(os.path.join(self.data_path('input'),"cricket.wav"),sr=16000)

    def get_window_length(self,max_slice = 5):
        print(f"[-] Break the audio into chunks of 5 seconds")
        self.window_length = max_slice * self.sr

    def get_short_time_energy(self):
        print(f"[-] Calculating the noise of every frame")
        self.energy = np.array([sum(abs(self.x[i:i+self.window_length]**2)) for i in range(0, len(self.x), self.window_length)])

    def get_threshold(self,energy):
        median, q3, iqr  = np.median(energy) , np.quantile(energy , 0.75) , np.quantile(energy, 0.75) - np.quantile(energy, 0.25)
        multiplication_rate = 2.5
        start , end = int(median) , int(q3 + (multiplication_rate * iqr))
        return (start + end) / 2

    def select_shots(self):
        print(f"[-] Selecting the shots based on threshold value")
        energy = self.energy
        self.df=pd.DataFrame(columns=['energy','start','end'])
        threshold = self.get_threshold(energy)
        row_index=0
        for i in range(len(energy)):
            value=energy[i]
            if(value>=threshold):
                i=np.where(energy == value)[0]
                self.df.loc[row_index,'energy']=value
                self.df.loc[row_index,'start']=i[0] * 5
                self.df.loc[row_index,'end']=(i[0]+1) * 5
                row_index= row_index + 1

    def merge(self):
        print(f"[-] Merge consecutive time intervals of audio clips into one")
        temp,i,j,df=[],0,0,self.df
        n,m=len(df) - 2 , len(df) -1
        while(i<=n):
            j=i+1
            while(j<=m):
                if(df['end'][i] == df['start'][j]):
                    df.loc[i,'end'] = df.loc[j,'end']
                    temp.append(j)
                    j=j+1
                else:
                    i=j
                    break      

        df.drop(temp,axis=0,inplace=True)
        self.df = df

    def generate_highlight(self,filename):
        print(f"[-] Extract the video within a particular time interval to form highlights")
        start=np.array(self.df['start'])
        end=np.array(self.df['end'])
        clips = []
        for i in range(len(self.df)):
            if(i!=0):
                # 5 = seconds
                start_lim = start[i] - 5
            else:
                start_lim = start[i] 
            end_lim = end[i]   
            clips.append(self.original_video.subclip(start_lim, end_lim))
            
        new_video = concatenate_videoclips(clips)
        new_video.write_videofile(os.path.join(self.data_path('output') , filename))

    def generate(self):
        filename = "highlights_" + self.dataset
        self.load_audio()
        # testing
        self.get_window_length()
        self.get_short_time_energy()
        self.select_shots()
        self.merge()
        self.generate_highlight(filename)
        