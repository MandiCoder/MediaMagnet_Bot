import re
from os import listdir, makedirs, unlink
from os.path import join, isdir
from modules.upload_files import uploadFile
from shutil import rmtree
from time import sleep
from yt_dlp import YoutubeDL
from unicodedata import normalize
from classes.google_drive import googleDrive
from .generate_words import generateWord
from .download_files import downloadFiles
from .database import read_db
from .compress_files import compressFiles

def autoUpload(app, msg, url, userbot):
    path_download = join('temp', generateWord(5))
    video_quality = read_db(msg.from_user.username)['video_quality']
    up_compress = read_db(msg.from_user.username)['up_compress']
    makedirs(path_download)
    
    downloadFiles(app, msg.chat.id, url, path_download, video_quality, userbot)
    
    if listdir(path_download) == 1:
        for i in listdir(path_download):
            file = join(path_download, i)
            uploadFile(app, msg, file, msg.from_user.username)
            sleep(5)
            if isdir(file):
                list_files = []
                for i in listdir(path_download): 
                    list_files.append(join(path_download, file, i))
                compressFiles(app, msg, list_files, file, './')    
                uploadFile(app, msg, file + ".zip", msg.from_user.username)
                unlink(file + ".zip")
    else:
        if up_compress:
            list_files = []
            for file in listdir(path_download): 
                list_files.append(join(path_download, file))
            name = getName(url)
            compressFiles(app, msg, list_files, name, './')
            uploadFile(app, msg, name + ".zip", msg.from_user.username)
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