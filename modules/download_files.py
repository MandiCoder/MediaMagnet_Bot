import yt_dlp
from .progres_bar import progressddl, progresswget
from .mediafire import get as getmf
from time import time
from classes.get_info import getInfo
from unicodedata import normalize
from os.path import join, basename
from modules.wget import download
from user_agent import generate_user_agent
from requests import get
from pyrogram.errors import ChannelInvalid






def downloadFiles(app, msg, usr, userbot):
    url = msg.text
    path_download = join('downloads', usr)
    
    ##################################################### DESCARGAR VIDEOS SHORTS DE YOUTUBE
    if 'https://youtu' and 'short' in url:
        sms = msg.reply("Descargando...")
        info = getInfo(url)
        title = normalize("NFKD", info.title).encode("ascii", "ignore").decode("utf-8", "ignore")
        title = title.replace(" ", "_").replace("(", "").replace(")", "")
        
        options = {
            'format': 'best',
            'outtmpl': join(path_download, title+'.%(ext)s')    
        }
        with yt_dlp.YoutubeDL(options) as ydl: ydl.download([url]) 
        sms.delete()    
        
    
    
    
    
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
            sms.edit_text("✅ **Descarga completa**")
        except Exception as x:
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")
        




    
    ###################################################### DESCARGAR ARCHIVOS DE ENLACE DIRECTO
    elif url.startswith("http") and "t.me/" not in url:
        sms = msg.reply("📥 **Descargando archivo...**")
        try:
            filename = download(url, sms, app, out=path_download, bar=progresswget)  
            sms.edit_text("✅ **Descarga completa**")
        except:
            try:
                r = get(url, headers={"user-agent": generate_user_agent()})
                with open(f"{usr}/{basename(url)}", "wb") as f: f.write(r.content)
                sms.edit_text("✅ **Descarga completa**")
            except Exception as x:
                sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")




    ###################################################### DESCARGAR ARCHIVOS DE CANALES REESTRINGIDOS
    if url.startswith("https://t.me/"):
        sms = msg.reply("📥 **Descargando archivo...**")
        if url.endswith("?single"): url = url.replace("?single", "")

        if url.startswith("https://t.me/c/"):
            try:
                chat = "-100" + url.split("/")[-2]
                msg_id = url.split("/")[-1]
                msge = userbot.get_messages(int(chat), int(msg_id))
                if msge.media:
                    start = time()
                    file = userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
                    sms.edit_text("✅ **Descarga completa**")
            except ChannelInvalid:
                try: sms.delete()
                except: pass
                sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")
        else:
            try:
                chat = url.split("/")[-2]
                msg_id = url.split("/")[-1]
                msge = userbot.get_messages(chat, int(msg_id))
                if msge.media:
                    start = time()
                    file = userbot.download_media(msge, file_name=f"{path_download}/", progress=progressddl, progress_args=(sms, start, 0))
                    sms.edit_text("✅ **Descarga completa**")
            except ChannelInvalid:
                try: sms.delete()
                except: pass
                sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")

        