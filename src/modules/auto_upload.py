import re
from os import listdir, makedirs, unlink
from os.path import join, isdir
from src.modules.upload_files import uploadFile
from shutil import rmtree
from time import sleep
from yt_dlp import YoutubeDL
from unicodedata import normalize
from src.classes.google_drive import googleDrive
from .generate_words import generateWord
from .download_files import downloadFiles
from .database import read_db
from .compress_files import compressFiles

def autoUpload(app, msg, url, userbot):
    path_download = join('temp', generateWord(5))
    video_quality = read_db(msg.from_user.username)['video_quality']
    up_compress = read_db(msg.from_user.username)['up_compress']
    makedirs(path_download)
    
    sms = downloadFiles(app, msg.chat.id, url, path_download, video_quality, userbot)
    sms.delete()

    if len(listdir(path_download)) == 1:
        for i in listdir(path_download):
            file = join(path_download, i)
            if isdir(file):
                list_files = []
                for j in listdir(file): 
                    list_files.append(join(file, j))  
                sms = compressFiles(app, msg, list_files, i, './')
                rmtree(path_download)
                uploadFile(app, msg, i + '.zip', msg.from_user.username)
                sms.delete()
                unlink(i + '.zip')
            else:
                uploadFile(app, msg, file, msg.from_user.username)
            sleep(5)
    else:
        print('Comprimiendo..')
        if up_compress:
            list_files = []
            for file in listdir(path_download): 
                list_files.append(join(path_download, file))
            name = getName(url)
            sms = compressFiles(app, msg, list_files, name, './')
            rmtree(path_download)
            uploadFile(app, msg, name + ".zip", msg.from_user.username)
            sms.delete()
            unlink(name+ ".zip")
        else:    
            for i in listdir(path_download):
                file = join(path_download, i)
                uploadFile(app, msg, file, msg.from_user.username)
                sleep(5)
            
    rmtree(path_download)
    
    


    
def getName(url:str) -> str:
    name = ''
    if "drive.google.com" in url:
        if url.endswith('drive_link'):
            folder_id = url.split('/')[-1].split('?')[0]
        else:
            folder_id = url.split('/')[-1]
            
        drive = googleDrive().login()
        name = drive.CreateFile({'id': folder_id})['title']
        
    elif 'https://youtu' in url:
        ydl_opts = {'ignoreerrors': True}
        
        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            name = playlist_info.get('title')
        
    return cleanString(name)





def cleanString(string:str) -> str:
    text = normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8", "ignore")
    text = re.sub(r'[\[\]\(\)]', '', text)
    return text