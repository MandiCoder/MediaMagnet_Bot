from .progres_bar import progressupl
from os.path import getsize, exists, join, basename
from os import makedirs, listdir, unlink
from modules.database import read_db
from modules.compress import split, getBytes
from pyrogram import enums
from time import time

def uploadFile(app, msg, file, username):
    size_file = read_db(username)["zip_size"]

    if (round(getsize(file) / 1000000, 2) > size_file):
        splitFiles(app, msg, file, username, size_file)
        
    else:
        sms = msg.reply(f"**🚀 Subiendo: {basename(file)}**")
        chat_id = msg.chat.id
        start = time()
        app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_DOCUMENT)
        app.send_document(
            chat_id,
            file,
            progress=progressupl,
            progress_args=(sms, 1, 1, start),
        )
        sms.delete()

        
        

def splitFiles(app, msg, file, username, size_file):
    path_zip = join('downloads', 'folder_zip', username)
    chat_id = msg.chat.id

    if not exists(path_zip): makedirs(path_zip)

    sms = msg.reply(f'**Subiendo: `{file.split("/")[-1]}`...**')
    sms.edit(f"✂️ **Dividiendo en partes de: {size_file} MB**") 

    split(file, path_zip, getBytes(f"{size_file}.0MiB"))
    list_files = listdir(path_zip)
    sms.delete()
    pin = sms.reply(f'**📌 {basename(file)}**')
    
    for count, file in enumerate(list_files):
        path_file = join(path_zip, file)
        sms = msg.reply(f"**🚀 Subiendo: {count+1}-{len(list_files)}**")
        app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_DOCUMENT)
        start = time()
        app.send_document(
            chat_id, 
            path_file, 
            progress=progressupl, 
            progress_args=(sms, len(list_files), count+1, start)
            )
        unlink(path_file)
        sms.delete()