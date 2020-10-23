from pytube import YouTube
from pytube.cli import on_progress
import os

class youtube():
    def __init__(self,url):
        self.url = url

    def downlaod_path(self):
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        input_path = os.path.join(parent_dir , 'data','input')
        return input_path

    def download(self):
        print(f"[-] DOWNLOADING YOUTUBE VIDEO")
        # try for 5 times
        times = 5
        for i in range(times):
            try:
                # making object of youtube class,
                # on_progress_callback will show downloading on CLI
                yt = YouTube(self.url,on_progress_callback=on_progress)
                # download 720p or 480p video
                
                video = yt.streams.filter(progressive = True,file_extension = 'mp4').order_by('resolution').desc().first()
                input_path = self.downlaod_path()
                video.download(input_path,filename='input_video')
                return 'input_video.mp4'
            except:
                print(f"[-] Could not download")
                print(f"[-] {times-i+1} tries left")
            
        return 'failed'





""" if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=WgoanhMvjx0'
    yt = youtube(url)
    yt.download() """