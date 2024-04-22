from pytube import YouTube

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(f"Progreso: {percentage_of_completion:.2f}%")


url = "https://youtu.be/0bqzZARdX14?si=CV12aikU0jJoTNqY"

yt = YouTube(url, on_progress_callback=on_progress)
title = yt.title
video = yt.streams.get_audio_only()
file = video.download(output_path="downloads/MandiCoder", filename=f"{title}.mp3")