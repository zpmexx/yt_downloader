from pytube import Playlist, YouTube
import os

# Your playlist URL


# List to store successful downloads and dictionary to store failed downloads
succedPlaylistList = []
failPlaylistDict = {}
def downloadPlaylist(playlist_url):
#playlist_url = "https://youtube.com/playlist?list=PL7MLhOHeVv7tqsPi0HwgSlPgARfxZKByt&si=wVrGHkl5Yuq2kNTB"
    try:
        playlist = Playlist(playlist_url)
        for video in playlist.video_urls:
            try:
                yt = YouTube(video)
                audio_stream = yt.streams.filter(only_audio=True).first()

                destination = './pobrane'

                out_file = audio_stream.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                succedPlaylistList.append(video)
            except Exception as e:
                failPlaylistDict[video] = str(e)

    except Exception as e:
        return f'(Problem z pobraniem playlisty: {e}', _
    
    return succedPlaylistList, failPlaylistDict


