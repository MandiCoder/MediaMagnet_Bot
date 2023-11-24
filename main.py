# MIS MODULOS
from modules.download_files_telegram import download_files_telegram
from modules.pyrogram_init import PyrogramInit
from modules.show_files import showFiles
from modules.global_variables import *
from modules.download_files import downloadFiles
from modules.upload_files import uploadFile
from modules.database import create_db
# MODULOS EXTERNOS
from pyrogram import filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from os.path import exists, join, basename
from os import mkdir, unlink, rename, listdir
from queue import Queue as cola

bot = PyrogramInit()

@bot.app.on_message(filters.command('start'))
def enviar_mensajes(app, msg):
    btn = ReplyKeyboardMarkup([
        ['📁 Archivos', '⚙️ Opciones'],
        ['📤 Subir todo', '🗂 Subir album'],
        ['🗑 BORRAR TODO']
    ], resize_keyboard=True, one_time_keyboard=True)
    
    create_db(msg.from_user.username)
    msg.reply('Bienvenido a mi bot :v', reply_markup=btn)
    

    
    
    
# ------------------------------------------------------------------------- VER ARCHIVOS DESCARGADOS
@bot.app.on_message(filters.regex('📁 Archivos'))
def mostrar_archivos(app, msg):
    showFiles(msg, msg.from_user.username)





# ------------------------------------------------------------------------- BORRAR TODOS LOS ARCHIVOS
@bot.app.on_message(filters.regex('🗑 BORRAR TODO'))
def borrar_todo(app, msg):
    for c, i in enumerate(listdir(msg.from_user.username)):
        c+1
        unlink(join(msg.from_user.username, i))
    msg.reply(f'**✅ {c+1} Archivos eliminados**')
    
    
    
    
    
# ---------------------------------------------------------------------- DESCARGAR ARCHIVOS Y VIDEOS
@bot.app.on_message(filters.regex('http'))
def descargar_archivos(app, msg):
    if not exists(msg.from_user.username): mkdir(msg.from_user.username)
    downloadFiles(app, msg, msg.from_user.username, bot.user_bot)
    showFiles(msg, msg.from_user.username)
    





# ------------------------------------------------------------------------- OPCIONES DEL ARCHIVO
@bot.app.on_message(filters.regex("/op_"))
def opcionesArchivo(app, msg):
    file = userFiles[msg.from_user.username][int(msg.text.split('_')[-1])]
    url = f"https://{bot.NAME_APP}.onrender.com/file/{msg.from_user.username}/{file}".replace(' ', '%20')
    # http://127.0.0.1:8000/file/KOD_16/
    
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton('⬆️ SUBIR ARCHIVO', callback_data=f'upload {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🔗 ENLACE', url=url)],
    ])
    msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=btn)





# ------------------------------------------------------------------------ RENOMBRAR ARCHIVO 📝
@bot.app.on_callback_query(filters.create(lambda f, c, u: "rename" in u.data))
def renombrarArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    callback.message.reply(f'**📝 Introduce el nuevo nombre para: `{basename(file)}`**', 
                          reply_markup=ForceReply(placeholder='Nuevo nombre'))

@bot.app.on_message(filters.reply)
def cambiarNombre(app, msg):
    rename(join(msg.from_user.username, msg.reply_to_message.text.split(': ')[-1]), 
           join(msg.from_user.username, msg.text))
    
    msg.reply(f'✅ Nombre cambiado a: `{msg.text}')
    showFiles(msg, msg.from_user.username)




# ------------------------------------------------------------------------- SUBIR UN ARCHIVO ⬆️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "upload" in u.data))
def subirArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
   
    
    uploadFile(app, callback.message, file, callback.from_user.username)





# ---------------------------------------------------------------------- ELIMINAR UN ARCHIVO 🚮
@bot.app.on_callback_query(filters.create(lambda f, c, u: "del_file" in u.data))
def elimiarArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    unlink(file)
    callback.message.edit(f'✅ {basename(file)} eliminado')
    showFiles(callback.message, callback.from_user.username)




# ---------------------------------------------------------------------- DESCARGAR ARCHIVOS DE TELEGRAM
@bot.app.on_message(filters.media & filters.private)
def descargarArchivosTelegram(app, message):
    username = message.from_user.username
    path_user = join('downloads', username)

    if username in download_queues:
        download_queues[username].put( (message, path_user) )
    else:
        queue = cola()
        queue.put( (message, path_user) )
        download_queues[username] = queue
        download_files_telegram(app, username)



if __name__ == '__main__':
    bot.iniciar_bot()