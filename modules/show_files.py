from os import listdir, rename
from os.path import join, isfile, getsize, dirname
from modules.global_variables import userFiles, user_path
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from unicodedata import normalize
import re


def showFiles(msg, usr, path_user):
    list_files = "**--📁 Archivos descargados--**\n"
    total_size = 0
    file_list = {}
    
    if usr not in user_path:
        path_user = join('downloads', usr)
    else:
        path_user = user_path[usr]
        
    btn = [ [InlineKeyboardButton('🗑 BORRAR TODO', callback_data='borrar_todo')] ]
    
    if 'downloads' == dirname(path_user):
        btn = [ [InlineKeyboardButton('🗑 BORRAR TODO', callback_data='borrar_todo')] ]
        
    else:
        btn = [
            [InlineKeyboardButton('🗑 BORRAR TODO', callback_data='borrar_todo')],
            [InlineKeyboardButton('⬅️ ATRAS', callback_data='atras')]
        ]
        
    for count, file in enumerate(listdir(path_user)):
        path_files = join(path_user, file)
        try:
            path_files = cleanString(path_files)
        except Exception as e: 
            print(e)
            
        if isfile(path_files):
            size = round(getsize(path_files) / 1000024, 2)
            list_files += (f"\n❯ **/op_{count+1} - {size} MB - `{file}`**\n")
            total_size += size
        else:
            list_files += (f"\n🗂 **/op_{count+1} - `{file}`**\n")
            
        file_list[count+1] = path_files
        userFiles[usr] = file_list
        
    sms = msg.reply(list_files, reply_markup=InlineKeyboardMarkup(btn))
    return sms


def cleanString(string:str) -> str:
    text = normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8", "ignore")
    text = re.sub(r'[\[\]\(\)]', '', text)
    rename(string, text)
    return text