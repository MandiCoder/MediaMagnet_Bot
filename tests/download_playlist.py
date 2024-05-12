from pytube import Playlist



def descargar_playlist(url):

    playlist = Playlist(url)
    num_videos = len(playlist.video_urls)
    for video in playlist.videos:
        print(f"Descargando: {video.title}\nRestantes: {num_videos}")
        num_videos -= 1
        try:
            video.streams.get_highest_resolution().download(output_path="downloads/MandiCoder")
        except:
            print("Error")

# Reemplaza 'url_de_tu_playlist' con la URL de tu lista de reproducción de YouTube
descargar_playlist("https://youtube.com/playlist?list=PL0gZ8Ba6dZ7KqKGpl97skDQ06hmk3vq7L&si=QqfaqbQdafcyQ_2k")
