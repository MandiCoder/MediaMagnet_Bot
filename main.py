# MIS MODULOS
from modules.pyrogram_init import PyrogramInit
from modules.functions import *
from modules.global_variables import *
from modules.download_files import downloadFiles
from modules.upload_files import uploadFile
# MODULOS EXTERNOS
from pyrogram import filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from os.path import exists, join, basename
from os import mkdir, unlink, rename
from queue import Queue as cola

bot = PyrogramInit()

@bot.app.on_message(filters.command('start'))
def enviar_mensajes(app, msg):
    btn = ReplyKeyboardMarkup([
        ['📁 Archivos', '⚙️ Opciones'],
        ['📤 Subir todo', '🗂 Subir album'],
        ['🗑 BORRAR TODO']
    ], resize_keyboard=True, one_time_keyboard=True)
    
    msg.reply('Bienvenido a mi bot :v', reply_markup=btn)
    

    
    
    
# ------------------------------------------------------------------------- VER ARCHIVOS DESCARGADOS
@bot.app.on_message(filters.regex('📁 Archivos'))
def mostrar_archivos(app, msg):
    if not exists(msg.from_user.username): mkdir(msg.from_user.username)
    showFiles(app, msg, msg.from_user.username, bot.NAME_APP)





# ------------------------------------------------------------------------- VER ARCHIVOS DESCARGADOS
@bot.app.on_message(filters.regex('🗑 BORRAR TODO'))
def borrar_todo(app, msg):
    for c, i in enumerate(msg.from_user.username):
        c+1
        join(msg.from_user.username, i)
    msg.reply(f'**✅ {c} Archivos eliminados**')
    
    
    
    
    
# ---------------------------------------------------------------------- DESCARGAR ARCHIVOS Y VIDEOS
@bot.app.on_message(filters.regex('http'))
def descargar_archivos(app, msg):
    if not exists(msg.from_user.username): mkdir(msg.from_user.username)
    downloadFiles(app, msg, msg.from_user.username)
    
    





# ------------------------------------------------------------------------- OPCIONES DEL ARCHIVO
@bot.app.on_message(filters.regex("/op_"))
def opcionesArchivo(app, msg):
    file = userFiles[msg.from_user.username][int(msg.text.split('_')[-1])]
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton('⬆️ SUBIR ARCHIVO', callback_data=f'upload {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
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
    showFiles(app, msg, msg.from_user.username,)




# ------------------------------------------------------------------------- SUBIR UN ARCHIVO ⬆️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "upload" in u.data))
def subirArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    uploadFile(app, callback.message, file)





# ---------------------------------------------------------------------- ELIMINAR UN ARCHIVO 🚮
@bot.app.on_callback_query(filters.create(lambda f, c, u: "del_file" in u.data))
def elimiarArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    unlink(file)
    callback.message.edit(f'✅ {basename(file)} eliminado')





# ---------------------------------------------------------------------- DESCARGAR ARCHIVOS DE TELEGRAM
@bot.app.on_message(filters.media & filters.private)
def descargarArchivosTelegram(app, message):
    if message.from_user.username in download_queues:
        download_queues[message.from_user.username].put( (message, message.from_user.username) )
    else:
        queue = cola()
        queue.put( (message, message.from_user.username) )
        download_queues[message.from_user.username] = queue
        download_files_telegram(app, message.from_user.username)



if __name__ == '__main__':
    bot.iniciar_bot()