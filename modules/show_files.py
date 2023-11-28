from os import listdir, makedirs, rename
from os.path import join, isfile, getsize, exists
from modules.global_variables import userFiles
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from unicodedata import normalize
import re


def showFiles(msg, usr):
    list_files = "**--📁 Archivos descargados--**\n"
    total_size = 0
    file_list = {}

    path_user = join('downloads', usr)
    
    if not exists(path_user): 
        makedirs(path_user)

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton('🗑 BORRAR TODO', callback_data='borrar_todo')]
    ])
    for count, file in enumerate(listdir(path_user)):
        path_files = join(path_user, file)
        if isfile(path_files):
            try:
                path_files = cleanString(path_files)
            except Exception as e: 
                print(e)
            size = round(getsize(path_files) / 1000024, 2)
            list_files += (f"\n❯ **/op_{count+1} - {size} MB - `{file}`**\n")
            total_size += size
            file_list[count+1] = path_files
            
        userFiles[usr] = file_list
        
    msg.reply(list_files, reply_markup=btn)    


def cleanString(string:str) -> str:
    text = normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8", "ignore")
    text = re.sub(r'[\[\]\(\)]', '', text)
    rename(string, text)
    return text