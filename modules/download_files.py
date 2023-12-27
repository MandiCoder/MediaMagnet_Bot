import yt_dlp
from modules.wget import download
from .progres_bar import  progresswget, progressytdl
from .mediafire import get as getmf
from .youtubedl_mod import YoutubeDL
# from time import time
from os.path import join, basename
from user_agent import generate_user_agent
from requests import get
# from pyrogram.errors import ChannelInvalid






def downloadFiles(app, chat_id, url, path_download, video_quality):
    
    ##################################################### DESCARGAR VIDEOS SHORTS DE YOUTUBE
    if 'https://youtu' in url and 'short' in url:
        try:
            sms = app.send_message(chat_id, "🚚 **Descargando...**")
            options = {
                'format': 'best',
                'outtmpl': join(path_download, '%(title)s.%(ext)s')    
            }
            
            with yt_dlp.YoutubeDL(options) as ydl: 
                ydl.download([url]) 
                
            return sms
        except Exception as x:
            print(x)
            app.send_message(chat_id, x)
            
        return sms
        
        
    ###################################################### DESCARGAR VIDEOS DE YOUTUBE
    if 'https://youtu' in url:
        sms = app.send_message(chat_id, "**🚚 Descargando video**")
        ytdl = YoutubeDL(progressytdl, sms, app, False)
        ytdl.download(url, path_download, video_quality)
    
        return sms
    
    
    
    ###################################################### DESCARGAR REELS DE INSTAGRAM
    elif 'instagram.com' in url:
        # https://www.instagram.com/reel/CzMSJ6Pxbte/?igshid=MTM5ZmplcXBiN2h5Nw==
        # https://www.ddinstagram.com/reel/Cwdc8zRoPlJ/?igshid=NTc4MTIwNjQ2YQ==
        app.send_message(chat_id, url.replace('instagram', 'ddinstagram'), disable_web_page_preview=False)
        
        
        
        
    ###################################################### DESCARGAR ARCHIVOS DE MEDIAFIRE
    elif "mediafire" in url:
        sms = app.send_message(chat_id, "📥 **Descargando archivo...**")
        try:
            download(getmf(url), sms, app, out=path_download, bar=progresswget)
            return sms
        except Exception as x:
            print(x)
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")

        return sms
    
    ###################################################### DESCARGAR ARCHIVOS DE ENLACE DIRECTO
    elif url.startswith("http") and "t.me/" not in url:
        sms = app.send_message(chat_id, "📥 **Descargando archivo...**")
        try:
            download(url, sms, app, out=path_download, bar=progresswget)  
            
        except Exception as e:
            print(e)
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{e}** ❌")
            try:
                r = get(url, headers={"user-agent": generate_user_agent()})
                with open(f"{path_download}/{basename(url)}", "wb") as f: 
                    f.write(r.content)
                return sms
            except Exception as e:
                print(e)
                sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{e}** ❌")
                
        return sms



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
                    
    #             sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")
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
    #             sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")

        