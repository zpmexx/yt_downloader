# Importing packages
import os
from yt_dlp import YoutubeDL
import os 
from datetime import datetime
# Define the destination folder for downloads
destination_folder = './downloaded/'

def downloadSongs(songList):
    """Downloads individual songs from the given list of URLs."""
    succedList = []
    failDict = {}
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
    }

    for song in songList:
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([song])
                succedList.append(song)
                print(f"Downloaded successfully: {song}")
        except Exception as e:
            failDict[song] = str(e)
            print(f"Failed to download: {song}, Error: {e}")

    return succedList, failDict


def downloadPlaylist(playlist_urls):
    """Downloads playlists by iterating over individual video URLs."""
    succedPlaylistList = []
    failPlaylistDict = {}
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(destination_folder, '%(playlist_title)s/%(title)s.%(ext)s'),
    }

    for playlist_url in playlist_urls:
        print(f"Processing playlist: {playlist_url}")
        try:
            # Extract playlist information
            with YoutubeDL({'quiet': True}) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)

            # Check if the URL is a valid playlist
            if 'entries' not in playlist_info:
                raise ValueError("The provided URL is not a valid playlist.")

            # Iterate through video entries in the playlist
            for entry in playlist_info['entries']:
                try:
                    video_url = entry['url']
                    print(f"Processing video: {entry['title']} ({video_url})")
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                        succedPlaylistList.append(video_url)
                        print(f"Downloaded video successfully: {entry['title']}")
                except Exception as e:
                    failPlaylistDict[entry['url']] = str(e)
                    print(f"Failed to download video: {entry['title']}, Error: {e}")

        except Exception as e:
            failPlaylistDict[playlist_url] = str(e)
            print(f"Failed to process playlist: {playlist_url}, Error: {e}")

    print("Summary:")
    print(f"Successful: {len(succedPlaylistList)}")
    print(f"Failed: {len(failPlaylistDict)}")
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

    

