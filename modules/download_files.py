import yt_dlp
from classes.get_info import getInfo
from unicodedata import normalize
from os.path import join
from os import listdir

def downloadFiles(app, msg, usr):
    sms = msg.reply("Descargando...")
    URL = msg.text
    
    
    # DESCARGAR VIDEOS SHORTS DE YOUTUBE
    if URL.startswith('https://youtu') and 'short' in URL:
        info = getInfo(URL)
        title = normalize("NFKD", info.title).encode("ascii", "ignore").decode("utf-8", "ignore")
        title = title.replace(" ", "_").replace("(", "").replace(")", "")
        
        options = {
            'format': 'best',
            'outtmpl': join(usr, title+'.%(ext)s')    
        }
        
        with yt_dlp.YoutubeDL(options) as ydl: ydl.download([URL])

        for i in listdir(usr):
            if title in i: title = i
            
        sms.delete()    
        return title
        