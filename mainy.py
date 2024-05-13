# importing packages 
from pytube import YouTube 
import os 
from datetime import datetime
# url input from user 

songList = []
filesContent = ''
with open ('files.txt','r')as file:
    # filesContent = file.read()
    # file.seek(0)
    for link in file.readlines():
        songList.append(link.strip())

songList = list(set(songList))

succedList = []
failDict = {}
for song in songList:
    try:
        yt = YouTube(song) 
        video = yt.streams.filter(only_audio=True).first() 
        destination = './pobrane'
        out_file = video.download(output_path=destination) 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
        succedList.append(song)
    except Exception as e:
        failDict[song] = e

current_date_time = datetime.now()
formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")

source_file = "files.txt"
destination_file = "download_history.txt"

with open(destination_file, 'a') as file:
    formatted_date_time_string = f"{formatted_date_time}\n"
    succedList_string = '\n'.join(str(song) for song in succedList) + '\n'
    separator_string = '-' * 50 + '\n'
    failed_downloads_string = '\n'.join([f"{key} - {value}" for key, value in failDict.items()]) 
    fileContent = formatted_date_time_string
    
    succedList_stringNoNewLine = succedList_string.replace('\n', "")
    failed_downloads_stringNoNewLine = failed_downloads_string.replace('\n',"")
    
    if succedList_stringNoNewLine:
        fileContent += f'Udane pobrania:\n{succedList_string}{separator_string}'
    
    if failed_downloads_stringNoNewLine:
        fileContent += f'Nieudane pobrania:\n{failed_downloads_string}\n{separator_string}'
        
    fileContent += '\n'
    file.write(fileContent)
open(source_file, "w").close()

    

