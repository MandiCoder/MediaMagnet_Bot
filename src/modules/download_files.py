import yt_dlp
from .progres_bar import  progresswget, progressytdl, progressddl
from .mediafire import get as getmf
from .youtubedl_mod import YoutubeDL
from .torrentp import TorrentDownloader
from src.classes.google_drive import googleDrive
from src.modules.wget import download
from os.path import join, basename
from user_agent import generate_user_agent
from requests import get
from time import time
from pyrogram.errors import ChannelInvalid






def downloadFiles(app, chat_id, url, path_download, video_quality, userbot):
    options = {
                'format': 'best',
                'outtmpl': join(path_download, '%(title)s.%(ext)s')    
            }
    
    keywords = [
        "twitch",
        "fb.watch",
        "www.xvideos.com",
        "www.xnxx.com",
        "www.yourupload.com",
    ]
    
    try:
        sms = app.send_message(chat_id, "🚚 **Descargando archivo...**")

        if 'https://youtu' in url and 'short' in url: # -------------------------- DESCARGAR VIDEOS SHORTS DE YOUTUBE
            with yt_dlp.YoutubeDL(options) as ydl: 
                    ydl.download([url])



        elif 'https://youtu' in url and 'playlist?' in url: # ------------------------------------------- DESCARGAR PLAYLISTS DE YOUTUBE
            ytdl = YoutubeDL(progressytdl, sms, app, False)
            try:
                ytdl.downloadlist(url, path_download)
            except Exception as e:
                print(e)

        elif 'https://youtu' in url: # ------------------------------------------- DESCARGAR VIDEOS DE YOUTUBE
            ytdl = YoutubeDL(progressytdl, sms, app, False)
            format = ytdl.info(url)[-1]
            try:
                ytdl.download(url, path_download, video_quality)
            except Exception as e:
                print(e)
                ytdl.download(url, path_download, format.split(':')[0])

        if any(keyword in url for keyword in keywords): # ------------------------------------------- DESCARGAR VIDEOS DE YOUTUBE
            ytdl = YoutubeDL(progressytdl, sms, app, True)
            format = ytdl.info(url)[-1]
            try:
                ytdl.download(url, path_download, video_quality)
            except Exception as e:
                print(e)
                ytdl.download(url, path_download, format.split(':')[0])
            
            
            
        elif 'instagram.com' in url: # ------------------------------------------- DESCARGAR REELS DE INSTAGRAM
            app.send_message(chat_id, url.replace('instagram', 'ddinstagram'), disable_web_page_preview=False)
            return
        
        
        elif "drive.google.com" in url: # ---------------------------------------- DESCARGAR ARCHIVOS DE GOOGLE DRIVE
            googleDrive().download(url, path_download)

            
            
        elif "mediafire" in url: # ------------------------------------------------ DESCARGAR ARCHIVOS DE MEDIAFIRE
            download(getmf(url), sms, app, out=path_download, bar=progresswget)
            
            
            
        elif url.startswith('magnet:'): # ----------------------------------------- DESCARGAR ARCHIVOS DE TORRENT
            torrent_file = TorrentDownloader(url, path_download, sms)
            torrent_file.start_download()
        
        
        elif url.startswith("https://t.me/"): # ----------------------------------------- DESCARGA DE CANALES REESTRINGIDOS
            download_restricted(sms, url, userbot, path_download)
        
        
        elif url.startswith("http") and "t.me/" not in url: # ----------------------------------------- DESCARGAR ARCHIVOS DE ENLACE DIRECTO
            print("Descargando enlace:", url)
            download_http(app, sms, url, path_download)
        
        
        
        sms.edit_text("✅ **Descarga completa**")
        return sms
    except Exception as x:
            print(x)
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")
    
    
# DESCARGA DESDE HTTP    
def download_http(app, sms, url, path_download):
    try:
        download(url, sms, app, out=path_download, bar=progresswget)
    except Exception as e:
        print(e)
        r = get(url, headers={"user-agent": generate_user_agent()})
        with open(f"{path_download}/{basename(url)}", "wb") as f:
            f.write(r.content)







# DESCARGA DE CANALES REESTRINGIDOS
def download_restricted(sms, url, userbot, path_download):
    if url.endswith("?single"): 
        url = url.replace("?single", "")
        
    if url.startswith("https://t.me/c/"):
        try:
            chat = "-100" + url.split("/")[-2]
            msg_id = url.split("/")[-1]
            msge = userbot.get_messages(int(chat), int(msg_id))
            if msge.media:
                start = time()
                userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
        except ChannelInvalid:
            try: 
                sms.delete()
            except Exception as e:
                print(e) 
                
            sms.reply("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")
    else:
        try:
            chat = url.split("/")[-2]
            msg_id = url.split("/")[-1]
            msge = userbot.get_messages(chat, int(msg_id))
            if msge.media:
                start = time()
                userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
        except ChannelInvalid:
            try: 
                sms.delete()
            except Exception as e: 
                print(e)
            sms.reply("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")

        