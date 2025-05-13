import os
import asyncio
from yt_dlp import YoutubeDL
import time


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded/%(title)s.%(ext)s',
    'quiet': False,  # Set to True to silence output
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
def _download_song_sync(url):
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading: {url}")
        ydl.download([url])
        print("Done.")
    
        
def _download_playlist_sync(url):
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading playlist: {url}")
        ydl.download([url])
        print("Playlist downloaded.")
        
        
def extract_video_urls_from_playlist(url):
    ydl_opts_extract = {
        'quiet': True,
        'extract_flat': True,  # Do not download videos, just get metadata
        'force_generic_extractor': False,
    }
    with YoutubeDL(ydl_opts_extract) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        entries = info_dict.get('entries', [])
        video_urls = [entry['url'] for entry in entries if 'url' in entry]
        return video_urls

result = extract_video_urls_from_playlist('https://www.youtube.com/playlist?list=PL7MLhOHeVv7tPtFEjssZygIcek3z7p6IZ')
print(result)
        
        
        
        
        
        