import yt_dlp
from .progres_bar import progressddl, progresswget
from time import time
from classes.get_info import getInfo
from unicodedata import normalize
from os.path import join, basename
from modules.wget import download
from user_agent import generate_user_agent
from requests import get
from pyrogram.errors import ChannelInvalid





def downloadFiles(app, msg, usr, userbot):
    URL = msg.text
    
    ##################################################### DESCARGAR VIDEOS SHORTS DE YOUTUBE
    if 'https://youtu' and 'short' in URL:
        sms = msg.reply("Descargando...")
        info = getInfo(URL)
        title = normalize("NFKD", info.title).encode("ascii", "ignore").decode("utf-8", "ignore")
        title = title.replace(" ", "_").replace("(", "").replace(")", "")
        
        options = {
            'format': 'best',
            'outtmpl': join(usr, title+'.%(ext)s')    
        }
        with yt_dlp.YoutubeDL(options) as ydl: ydl.download([URL]) 
        sms.delete()    
        
    
    
    
    
    ###################################################### DESCARGAR REELS DE INSTAGRAM
    elif 'instagram.com' in URL:
        # https://www.instagram.com/reel/CzMSJ6Pxbte/?igshid=MTM5ZmplcXBiN2h5Nw==
        # https://www.ddinstagram.com/reel/Cwdc8zRoPlJ/?igshid=NTc4MTIwNjQ2YQ==
        msg.reply(URL.replace('instagram', 'ddinstagram'), disable_web_page_preview=False)
        
        
        
        
        
    ###################################################### DESCARGAR ARCHIVOS DE MEDIAFIRE
    elif "mediafire" in URL:
        sms = msg.reply("📥 **Descargando archivo...**")
        try:
            download(get(URL), sms, app, out=f"{usr}", bar=progresswget)
            sms.edit_text("✅ **Descarga completa**")
        except Exception as x:
            sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")
        




    
    ###################################################### DESCARGAR ARCHIVOS DE ENLACE DIRECTO
    elif URL.startswith("http") and "t.me/" not in URL:
        sms = msg.reply("📥 **Descargando archivo...**")
        try:
            filename = download(URL, sms, app, out=f"{usr}", bar=progresswget)  
            sms.edit_text("✅ **Descarga completa**")
        except:
            try:
                r = get(URL, headers={"user-agent": generate_user_agent()})
                with open(f"{usr}/{basename(URL)}", "wb") as f: f.write(r.content)
                sms.edit_text("✅ **Descarga completa**")
            except Exception as x:
                sms.edit_text(f"❌ **No se pudo descargar el archivo: \n{x}** ❌")




    ###################################################### DESCARGAR ARCHIVOS DE CANALES REESTRINGIDOS
    if URL.startswith("https://t.me/"):
        sms = msg.reply("📥 **Descargando archivo...**")
        if URL.endswith("?single"): URL = URL.replace("?single", "")

        if URL.startswith("https://t.me/c/"):
            try:
                chat = "-100" + URL.split("/")[-2]
                msg_id = URL.split("/")[-1]
                msge = userbot.get_messages(int(chat), int(msg_id))
                if msge.media:
                    start = time()
                    file = userbot.download_media(msge, file_name=f"{usr}/", progress=progressddl, progress_args=(sms, start, 0))
                    sms.edit_text("✅ **Descarga completa**")
            except ChannelInvalid:
                try: sms.delete()
                except: pass
                sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")
        else:
            try:
                chat = URL.split("/")[-2]
                msg_id = URL.split("/")[-1]
                msge = userbot.get_messages(chat, int(msg_id))
                if msge.media:
                    start = time()
                    file = userbot.download_media(msge, file_name=f"{usr}/", progress=progressddl, progress_args=(sms, start, 0))
                    sms.edit_text("✅ **Descarga completa**")
            except ChannelInvalid:
                try: sms.delete()
                except: pass
                sms.edit_text("**⚠️ PRIMERO DEBE INTRODUCIR EL ENLACE DE INVITACIÓN DEL CANAL**")

        