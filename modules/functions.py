from os import listdir
from os.path import join, isfile, getsize
from modules.global_variables import *
from time import sleep

def showFiles(app, msg, usr, name_app):
    
    listfiles = ""
    totalSize = 0
    fileList = {}
    
    for count, file in enumerate(listdir(usr)):
        count+=1
        if isfile(join(usr, file)):
            link = f"https://{name_app}.onrender.com/file/{usr}/{file}"
            size = round(getsize(join(usr, file)) / 1000024, 2)
            
            listfiles += (f"\n❯ **/op_{count} - {size} MB - [{file}]({link})**\n")
            
            totalSize += size
            fileList[count] = join(usr, file)
            
        userFiles[usr] = fileList
    
    msg.reply(listfiles)
    
    
    
    
def download_files_telegram(app, username):
    global download_queues
    
    queue = download_queues[username]
    folder_files = {username: []}

    while not queue.empty():
        sleep(3)
        message, directory = queue.get()
        sms = message.reply("**🚛 Downloading...**", quote=True)
        
        file = app.download_media(message=message, file_name=f"{directory}/",)
        folder_files[username].append(file.split("\\")[-1])
        sms.edit_text("✅ **Finished**")
        queue.task_done()
        
    del download_queues[username]
        
    