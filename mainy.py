import os
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloaded"
SONGS_FILE = "songs.txt"
PLAYLIST_FILE = "playlist.txt"

# Tworzenie folderu
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Opcje yt-dlp
ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': f'{DOWNLOAD_DIR}/%(playlist_title|NO_PLAYLIST)s/%(title)s.%(ext)s',
    'quiet': False,
    'ignoreerrors': True
}

def load_urls(file_path):
    """Wczytaj linki z pliku txt"""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def download_single_songs(urls):
    """Pobierz pojedyncze utwory"""
    if not urls:
        return

    print(f"\n=== Pobieranie pojedynczych utworów ({len(urls)}) ===\n")

    song_opts = ydl_opts.copy()
    song_opts['noplaylist'] = True

    with YoutubeDL(song_opts) as ydl:
        for url in urls:
            try:
                print(f"\nPobieranie utworu:\n{url}\n")
                ydl.download([url])
                print("OK")
            except Exception as e:
                print(f"Błąd: {e}")

def download_playlists(urls):
    """Pobierz playlisty"""
    if not urls:
        return

    print(f"\n=== Pobieranie playlist ({len(urls)}) ===\n")

    playlist_opts = ydl_opts.copy()
    playlist_opts['noplaylist'] = False

    with YoutubeDL(playlist_opts) as ydl:
        for url in urls:
            try:
                print(f"\nPobieranie playlisty:\n{url}\n")
                ydl.download([url])
                print("Playlista pobrana")
            except Exception as e:
                print(f"Błąd: {e}")

def main():
    song_urls = load_urls(SONGS_FILE)
    playlist_urls = load_urls(PLAYLIST_FILE)

    if not song_urls and not playlist_urls:
        print("Brak linków w songs.txt i playlist.txt")
        return

    download_single_songs(song_urls)
    download_playlists(playlist_urls)

    print("\n=== GOTOWE ===")

if __name__ == "__main__":
    main()