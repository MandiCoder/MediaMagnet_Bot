from .progres_bar import progressddl
from .global_variables import download_queues
from time import sleep, time
from os.path import basename



def download_files_telegram(app, username):
    global download_queues
    
    queue = download_queues[username]
    folder_files = {username: []}

    while not queue.empty():
        message, directory = queue.get()
        sms = message.reply("**🚛 Descargando...**", quote=True)
        sleep(3)
        
        start = time()
        file = app.download_media(message=message, 
                                  file_name=f"{directory}/",
                                  progress=progressddl, 
                                  progress_args=(sms, start, queue.qsize()),)
        
        folder_files[username].append(basename(file))
        sms.edit_text("✅ **Finished**")
        queue.task_done()
        
    del download_queues[username]