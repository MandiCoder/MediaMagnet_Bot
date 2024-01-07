import yt_dlp
from .progres_bar import  progresswget, progressytdl
from .mediafire import get as getmf
from .youtubedl_mod import YoutubeDL
from classes.google_drive import googleDrive
from modules.wget import download
from os.path import join, basename
from user_agent import generate_user_agent
from requests import get
from .torrentp import TorrentDownloader
# from pyrogram.errors import ChannelInvalid






def downloadFiles(app, chat_id, url, path_download, video_quality):
    
    options = {
                'format': 'best',
                'outtmpl': join(path_download, '%(title)s.%(ext)s')    
            }
    
    try:
        sms = app.send_message(chat_id, "🚚 **Descargando archivo...**")

        if 'https://youtu' in url and 'short' in url: # -------------------------- DESCARGAR VIDEOS SHORTS DE YOUTUBE
            with yt_dlp.YoutubeDL(options) as ydl: 
                    ydl.download([url])


        elif 'https://youtu' in url: # ------------------------------------------- DESCARGAR VIDEOS DE YOUTUBE
            ytdl = YoutubeDL(progressytdl, sms, app, False)
            ytdl.download(url, path_download, video_quality)
            
            
        elif 'instagram.com' in url: # ------------------------------------------- DESCARGAR REELS DE INSTAGRAM
            app.send_message(chat_id, url.replace('instagram', 'ddinstagram'), disable_web_page_preview=False)
            return
        
        
        elif "drive.google.com" in url: # ---------------------------------------- DESCARGAR ARCHIVOS DE GOOGLE DRIVE
            googleDrive(sms).download(url, path_download)

            
            
        elif "mediafire" in url: # ------------------------------------------------ DESCARGAR ARCHIVOS DE MEDIAFIRE
            download(getmf(url), sms, app, out=path_download, bar=progresswget)
            
            
            
        elif url.startswith('magnet:'): # ----------------------------------------- DESCARGAR ARCHIVOS DE TORRENT
            torrent_file = TorrentDownloader(url, path_download, sms)
            torrent_file.start_download()
        
        
        elif url.startswith("http") and "t.me/" not in url: # ----------------------------------------- DESCARGAR ARCHIVOS DE ENLACE DIRECTO
            download_http(app, sms, url, path_download)
        
        
        
        sms.edit_text("✅ **Descarga completa**")
    except Exception as x:
            print(x)
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")
    




def download_http(app, sms, url, path_download):
    try:
        download(url, sms, app, out=path_download, bar=progresswget)
    except Exception as e:
        print(e)
        r = get(url, headers={"user-agent": generate_user_agent()})
        with open(f"{path_download}/{basename(url)}", "wb") as f:
            f.write(r.content)









    # ###################################################### DESCARGAR ARCHIVOS DE CANALES REESTRINGIDOS
    # if url.startswith("https://t.me/"):
    #     sms = app.send_message(chat_id, "📥 **Descargando archivo...**")
    #     if url.endswith("?single"): 
    #         url = url.replace("?single", "")

    #     if url.startswith("https://t.me/c/"):
    #         try:
    #             chat = "-100" + url.split("/")[-2]
    #             msg_id = url.split("/")[-1]
    #             msge = userbot.get_messages(int(chat), int(msg_id))
    #             if msge.media:
    #                 start = time()
    #                 userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
    #                 return sms
    #         except ChannelInvalid:
    #             try: 
    #                 sms.delete()
    #             except Exception as e:
    #                 print(e) 
                    
    #             sms.reply("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")
    #     else:
    #         try:
    #             chat = url.split("/")[-2]
    #             msg_id = url.split("/")[-1]
    #             msge = userbot.get_messages(chat, int(msg_id))
    #             if msge.media:
    #                 start = time()
    #                 userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
    #                 return sms
    #         except ChannelInvalid:
    #             try: 
    #                 sms.delete()
    #             except Exception as e: 
    #                 print(e)
    #             sms.reply("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")

        