# importing packages 
from pytube import YouTube, Playlist
import os 
from datetime import datetime

destination_folder = './downloaded/'

def downloadSongs(songList):
    succedList = []
    failDict = {}
    for song in songList:
        try:
            yt = YouTube(song) 
            video = yt.streams.filter(only_audio=True).first() 
            destination = destination_folder
            out_file = video.download(output_path=destination) 
            base, ext = os.path.splitext(out_file) 
            new_file = base + '.mp3'
            os.rename(out_file, new_file) 
            succedList.append(song)
        except Exception as e:
            failDict[song] = e
    return succedList, failDict

def downloadPlaylist(playlist_url):
    succedPlaylistList = []
    failPlaylistDict = {}
    for playlist in playlist_url:
        print(playlist)
        try:
            playlist = Playlist(playlist)
            for video in playlist.video_urls:
                try:
                    yt = YouTube(video)
                    audio_stream = yt.streams.filter(only_audio=True).first()

                    destination = destination_folder

                    out_file = audio_stream.download(output_path=destination)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    succedPlaylistList.append(video)
                except Exception as e:
                    failPlaylistDict[video] = str(e)

        except Exception as e:
            failPlaylistDict[playlist] = str(e)
        
    return succedPlaylistList, failPlaylistDict


current_date_time = datetime.now()
formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")


separator_string = '-' * 50 + '\n'
fileContent = ''
song_source_file = "songs.txt"
destination_file = "download_history.txt"
formatted_date_time_string = f"{formatted_date_time}\n"
with open (destination_file, 'a') as file:
    file.write(formatted_date_time_string)

songList = []
try:
    with open ('songs.txt','r') as file:
        # filesContent = file.read()
        # file.seek(0)
        for link in file.readlines():
            songList.append(link.strip())
except:
    with open (destination_file, 'a') as file:
        file.write("Brak pliku songs.txt.\n")

songList = list(set(songList))
succedList, failDict = downloadSongs(songList)


if succedList or failDict:
    with open(destination_file, 'a') as file:
        succedList_string = '\n'.join(str(song) for song in succedList) + '\n'
        failed_downloads_string = '\n'.join([f"{key} - {value}" for key, value in failDict.items()]) 
        
        succedList_stringNoNewLine = succedList_string.replace('\n', "")
        failed_downloads_stringNoNewLine = failed_downloads_string.replace('\n',"")
        
        if succedList_stringNoNewLine:
            fileContent += f'Udane pobrania:\n{succedList_string}\n'
        
        if failed_downloads_stringNoNewLine:
            fileContent += f'{separator_string}Nieudane pobrania:\n{failed_downloads_string}\n{separator_string}'
            
        #fileContent += '\n'
        file.write(fileContent)
else:
    with open (destination_file, 'a') as file:
        file.write("Brak piosenek w pliku songs.txt.\n")
        
open(song_source_file, "w").close()        

playlist_source_file = 'playlist.txt'
playlistList = []
try:
    with open (playlist_source_file, 'r') as file:
        for playlist in file.readlines():
            playlistList.append(playlist.strip())
except:
    with open (destination_file, 'a') as file:
        file.write("Brak pliku playlist.txt.\n")
        
succedPlayList, failPlaylistDict = downloadPlaylist(playlistList)

fileContent = ''

if succedPlayList or failPlaylistDict:
    with open(destination_file, 'a') as file:
        succedPlaylist_string = '\n'.join(str(song) for song in succedPlayList) + '\n'
        failed_downloads_string = '\n'.join([f"{key} - {value}" for key, value in failPlaylistDict.items()]) 
        succedPlaylist_stringNoNewLine = succedPlaylist_string.replace('\n', "")
        failed_downloads_stringNoNewLine = failed_downloads_string.replace('\n',"")
        
        if succedPlaylist_stringNoNewLine:
            fileContent += f'Udane pobrania z playlisty:\n{succedPlaylist_string}\n'
        
        if failed_downloads_stringNoNewLine:
            fileContent += f'{separator_string}Nieudane pobrania z playlisty:\n{failed_downloads_string}\n'
            
        file.write(fileContent)
        
else:
    with open (destination_file, 'a') as file:
        file.write(f"Problem z pobraniem palylist z pliku playlist.txt.\n")

with open (destination_file, 'a') as file:
    file.write(f"{separator_string}")
    

open(playlist_source_file, "w").close()

    

