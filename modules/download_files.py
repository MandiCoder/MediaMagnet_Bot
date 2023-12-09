import yt_dlp
from modules.wget import download
from .progres_bar import  progresswget
from .mediafire import get as getmf
# from time import time
from os.path import join, basename
from user_agent import generate_user_agent
from requests import get
# from pyrogram.errors import ChannelInvalid






def downloadFiles(app, msg, path_download, url):
    
    ##################################################### DESCARGAR VIDEOS SHORTS DE YOUTUBE
    if 'https://youtu' in url:
        try:
            sms = msg.reply("🚚 **Descargando...**")
            options = {
                'format': 'best',
                'outtmpl': join(path_download, '%(title)s.%(ext)s')    
            }
            
            with yt_dlp.YoutubeDL(options) as ydl: 
                ydl.download([url]) 
                
            return sms
        except Exception as x:
            print(x)
            msg.reply(x)
        
        
    
    
    ###################################################### DESCARGAR REELS DE INSTAGRAM
    elif 'instagram.com' in url:
        # https://www.instagram.com/reel/CzMSJ6Pxbte/?igshid=MTM5ZmplcXBiN2h5Nw==
        # https://www.ddinstagram.com/reel/Cwdc8zRoPlJ/?igshid=NTc4MTIwNjQ2YQ==
        msg.reply(url.replace('instagram', 'ddinstagram'), disable_web_page_preview=False)
        
        
        
        
        
    ###################################################### DESCARGAR ARCHIVOS DE MEDIAFIRE
    elif "mediafire" in url:
        sms = msg.reply("📥 **Descargando archivo...**")
        try:
            download(getmf(url), sms, app, out=path_download, bar=progresswget)
            return sms
        except Exception as x:
            print(x)
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")


    
    ###################################################### DESCARGAR ARCHIVOS DE ENLACE DIRECTO
    elif url.startswith("http") and "t.me/" not in url:
        sms = msg.reply("📥 **Descargando archivo...**")
        try:
            download(url, sms, app, out=path_download, bar=progresswget)  
            sms.edit_text("✅ **Descarga completa**")
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




    # ###################################################### DESCARGAR ARCHIVOS DE CANALES REESTRINGIDOS
    # if url.startswith("https://t.me/"):
    #     sms = msg.reply("📥 **Descargando archivo...**")
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

        