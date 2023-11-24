from os import listdir, makedirs
from os.path import join, isfile, getsize, exists
from modules.global_variables import *
from pyrogram.types import ReplyKeyboardMarkup




def showFiles(msg, usr):
    
    list_files = "**--📁 Archivos descargados--**\n"
    total_size = 0
    file_list = {}

    path_user = join('downloads', usr)
    
    if not exists(path_user): makedirs(path_user)

    btn = ReplyKeyboardMarkup([
        ['📁 Archivos', '⚙️ Opciones'],
        ['📤 Subir todo', '🗂 Subir album'],
        ['🗑 BORRAR TODO']
    ], resize_keyboard=True, one_time_keyboard=True)
    
    for count, file in enumerate(listdir(path_user)):
        path_files = join(path_user, file)
        if isfile(path_files):
            size = round(getsize(path_files) / 1000024, 2)
            list_files += (f"\n❯ **/op_{count+1} - {size} MB - `{file}`**\n")
            total_size += size
            file_list[count+1] = path_files
            
        userFiles[usr] = file_list
        
    msg.reply(list_files, reply_markup=btn)    