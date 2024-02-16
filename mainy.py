# importing packages 
from pytube import YouTube 
import os 
  
# url input from user 

songList = []

with open ('files.txt','r')as file:
    for link in file.readlines():
        songList.append(link.strip())


for song in songList:
    yt = YouTube(song) 
    
    # extract only audio 
    video = yt.streams.filter(only_audio=True).first() 
    
    # check for destination to save file 
    destination = '.'
    
    # download the file 
    out_file = video.download(output_path=destination) 
    
    # save the file 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 
    
    

