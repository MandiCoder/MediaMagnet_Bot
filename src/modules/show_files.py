from os import listdir, rename, makedirs
from os.path import join, isfile, getsize, dirname, exists
from src.modules.global_variables import userFiles, user_path
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
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
    
    if not exists(path_user):
        makedirs(path_user)
        
    btn = [
        [InlineKeyboardButton(
                '🔗 ENLACES', 
                web_app=WebAppInfo(url=f'https://k53xxw3b-8000.usw3.devtunnels.ms/files/{usr}')
            )],
        [InlineKeyboardButton('🗑 BORRAR TODO', callback_data='borrar_todo')],
        [InlineKeyboardButton('☁️ SUBIR TODO A DRIVE', callback_data='subir_drive')]
    ]
    
    if 'downloads' != dirname(path_user):
        btn.append(
            [InlineKeyboardButton('⬅️ ATRAS', callback_data='atras')]
        )
        
    for count, file in enumerate(listdir(path_user)):
        path_files = join(path_user, file)
        try:
            path_files = cleanString(path_files)
        except Exception as e: 
            print(e)
            
        if isfile(path_files):
            size = getsize(path_files)
            list_files += (f"\n❯ **/op_{count+1} - {sizeof(size)} - `{file}`**\n")
            total_size += size
        else:
            list_files += (f"\n🗂 **/op_{count+1} - `{file}`**\n")
            
        file_list[count+1] = path_files
        userFiles[usr] = file_list
        
    list_files += f"\n**🗄 Total: `{sizeof(total_size)}`**"
    sms = msg.reply(list_files, reply_markup=InlineKeyboardMarkup(btn))
    return sms


def cleanString(string:str) -> str:
    text = normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8", "ignore")
    text = re.sub(r'[\[\]\(\)]', '', text)
    rename(string, text)
    return text

def sizeof(num: int, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)