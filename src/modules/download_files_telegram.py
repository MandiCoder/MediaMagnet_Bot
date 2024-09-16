from .progress import progress_download
from .global_variables import download_queues
from time import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from os.path import basename



def download_files_telegram(app, username):
    global download_queues
    
    queue = download_queues[username]
    folder_files = {username: []}

    while not queue.empty():
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 VER PROGRESO", callback_data="progress")],
            [InlineKeyboardButton("❌ CANCELAR", callback_data="cancel_progreso")]])
        
        
        message, directory = queue.get()
        sms = message.reply("**🚛 Descargando...**", quote=True, reply_markup=markup)
        start = time()
        file = app.download_media(
            message=message, 
            file_name=f"{directory}/",
            progress=progress_download, 
            progress_args=(username, app, start, queue.qsize())
        )
        
        folder_files[username].append(basename(file))
        sms.edit_text("✅ **Finished**")
        queue.task_done()
        
    del download_queues[username]