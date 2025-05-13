import os
import asyncio
from yt_dlp import YoutubeDL
import time

ffp_path = r"C:\Users\Z\Desktop\Porzadek\yt_ffmpeg\ffmpeg-2025-05-12-git-8ce32a7cbb-full_build\bin"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded/%(title)s.%(ext)s',
    'quiet': False,  # Set to True to silence output
    'noplaylist': True,
    'ffmpeg_location': ffp_path,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Download a single YouTube video as MP3
async def download_song(url: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _download_song_sync, url)

def _download_song_sync(url):
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading: {url}")
        ydl.download([url])
        print("Done.")

# Download all videos from a YouTube playlist as MP3
async def download_playlist(playlist_url: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _download_playlist_sync, playlist_url)

def _download_playlist_sync(url):
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading playlist: {url}")
        ydl.download([url])
        print("Playlist downloaded.")

# Example usage
async def main():
    start_time = time.time()
    print("start 2")
    urls = [
        "https://www.youtube.com/watch?v=XlM6VAhVEFw",
        "https://www.youtube.com/watch?v=88sARuFu-tc",
        "https://www.youtube.com/watch?v=sXJXLq1lN7U"
    ]
    await asyncio.gather(*(download_song(url) for url in urls))
    # await download_song("https://www.youtube.com/watch?v=XlM6VAhVEFw")
    # await download_song("https://www.youtube.com/watch?v=88sARuFu-tc")
    # await download_song("https://www.youtube.com/watch?v=sXJXLq1lN7U")
    #await download_playlist("https://www.youtube.com/playlist?list=PL7MLhOHeVv7tPtFEjssZygIcek3z7p6IZ")
    #await download_playlist("https://www.youtube.com/playlist?list=PL7MLhOHeVv7tPtFEjssZygIcek3z7p6IZ")
    end_time = time.time() - start_time
    print(f"Total time taken: {end_time:.2f} seconds")
# Run the script
if __name__ == '__main__':
    asyncio.run(main())
