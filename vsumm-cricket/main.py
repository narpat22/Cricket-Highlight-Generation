from highlights import highlight_generation
from download_youtube import youtube
import os

def select_input_type():
    return int(input(f"[-] 1 from Local Machine\n[-] 2 from Youtube\n[-] --> "))

def data_path():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    input_path = os.path.join(parent_dir , 'data','input')
    return input_path

if __name__ == "__main__":
    choice = select_input_type()
    if choice == 2:
        url = input(f"[-] Enter the URL --> ") 
        yt_download = youtube(url)
        filename = yt_download.download()
        if filename == 'failed':
            print('Could Not Download')
            exit()
    else: 
        filename = 'AUS-22-34.mp4'
    path = os.getcwd()
    vsumm = highlight_generation(path,filename)
    vsumm.generate()