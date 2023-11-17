from os import listdir
from os.path import join, isfile, getsize, basename
from modules.global_variables import *
from time import sleep, time as tm
from pyrogram.types import ReplyKeyboardMarkup
from .progres_bar import progressddl

def showFiles(app, msg, usr, name_app=None):
    
    listfiles = "**--📁 Archivos descargados--**\n"
    totalSize = 0
    fileList = {}
    
    btn = ReplyKeyboardMarkup([
        ['📁 Archivos', '⚙️ Opciones'],
        ['📤 Subir todo', '🗂 Subir album'],
        ['🗑 BORRAR TODO']
    ], resize_keyboard=True, one_time_keyboard=True)
    
    for count, file in enumerate(listdir(usr)):
        count+=1
        if isfile(join(usr, file)):
            link = f"https://{name_app}.onrender.com/file/{usr}/{file}"
            size = round(getsize(join(usr, file)) / 1000024, 2)
            
            listfiles += (f"\n❯ **/op_{count} - {size} MB - [{file}]({link})**\n")
            
            totalSize += size
            fileList[count] = join(usr, file)
            
        userFiles[usr] = fileList
        
        
    msg.reply(listfiles, reply_markup=btn)
    
    
    
    
def download_files_telegram(app, username):
    global download_queues
    
    queue = download_queues[username]
    folder_files = {username: []}

    while not queue.empty():
        message, directory = queue.get()
        sms = message.reply("**🚛 Descargando...**", quote=True)
        sleep(3)
        
        start = tm()
        file = app.download_media(message=message, 
                                  file_name=f"{directory}/",
                                  progress=progressddl, 
                                  progress_args=(sms, start, queue.qsize()),)
        
        folder_files[username].append(basename(file))
        sms.edit_text("✅ **Finished**")
        queue.task_done()
        
    del download_queues[username]
        
    