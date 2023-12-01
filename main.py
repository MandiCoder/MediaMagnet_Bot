# MIS MODULOS
from modules.download_files_telegram import download_files_telegram
from modules.pyrogram_init import PyrogramInit
from modules.show_files import showFiles
from modules.global_variables import btn_general, btn_opciones, userFiles, download_queues, access_bot
from modules.download_files import downloadFiles
from modules.upload_files import uploadFile
from modules.database import create_db, update_db, read_db
from modules.generate_words import generateWord
from modules.auto_upload import autoUpload

# MODULOS EXTERNOS
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from os.path import exists, join, basename
from os import makedirs, unlink, rename, listdir
from queue import Queue as cola


bot = PyrogramInit()

@bot.app.on_message(filters.command('start'))
def enviar_mensajes(app, msg):
    create_db(msg.from_user.username)

    if not msg.from_user.username == 'MandiCoder':
        msg.reply('Este bot solo lo puede usar su creador @MandiCoder 😛')
        return
    else: 
        msg.reply('Bienvenido a mi bot :v', reply_markup=btn_general)
    

    
    
    
# ------------------------------------------------------------------------- VER ARCHIVOS DESCARGADOS
@bot.app.on_message(filters.regex('📁 Archivos'))
def mostrar_archivos(app, msg):
    showFiles(msg, msg.from_user.username)





# ------------------------------------------------------------------------- BORRAR TODOS LOS ARCHIVOS 🗑
@bot.app.on_callback_query(filters.create(lambda f, c, u: "borrar_todo" in u.data))
def borrarTodo(app, callback):
    path_downloads = join('downloads', callback.from_user.username)
    c = 0
    for c, i in enumerate(listdir(path_downloads)):
        c+=1
        unlink(join(path_downloads, i))
    callback.message.reply(f'**✅ {c} Archivos eliminados**')
    
    
    
    

# ------------------------------------------------------------------------- OPCIONES GENERALES ⚙️
@bot.app.on_message(filters.regex('⚙️ Opciones'))
def mostrar_opciones(app, msg):
    
    text = f'Zip size: `{read_db(msg.from_user.username)["zip_size"]} MB`'
    msg.reply(f'**⚙️ Opciones:\n\n {text}**', reply_markup=btn_opciones)


# -------------------------------------------------- ZIP SIZE
@bot.app.on_callback_query(filters.create(lambda f, c, u: "zip_size" in u.data))
def zip_size(app, callback):
    callback.message.delete()
    callback.message.reply('📚 Introduzca el tamaño de los zips:', reply_markup=ForceReply())

@bot.app.on_message(filters.reply & filters.create(lambda f, c, u: u.reply_to_message.text.startswith('📚 Introduzca el tamaño de los zips:')))
def cambiarPesoZips(app, msg):
    zip_size = msg.text

    if zip_size.isdigit() :
        if int(zip_size) <= 2000 and int(zip_size) >= 10:
            update_db(username=msg.from_user.username, clave='zip_size', valor=zip_size)
            msg.reply(f'**✅ Zips establecidos en: `{zip_size} MB`', reply_markup=btn_general)
        else:
            msg.reply('**❌ ERROR: Debe introducir un numero --mayor-- que 10 y --menor-- que 2000**', reply_markup=btn_general)
    else:
        msg.reply('**❌ ERROR: Debe introducir un numero**', reply_markup=btn_general)
    
# ---------------------------------------------------------------------- DESCARGAR DE ENLACES
@bot.app.on_message(filters.create(lambda f, c, u: u.text.startswith('http')) & filters.private)
def descargar_archivos(app, msg):
    username = msg.from_user.username
    if username not in access_bot:
        path_download = join('temp', username, generateWord(5))
        autoUpload(app, msg, path_download, bot.user_bot, msg.text)  
    else:
        path_user = join('downloads', username)
        if not exists(path_user): 
            makedirs(path_user)
    
        sms = downloadFiles(app, msg, path_user, bot.user_bot, msg.text)
        sms.edit_text("✅ **Descarga completa**")

# ================================================ DESCARGAR ARCHIVOS EN CANALES
@bot.app.on_message(filters.command('dl'))
def descargarArchivosEnGrupos(app, msg):
    username = msg.from_user.username
    path_download = join('temp', username, generateWord(5))
    create_db(username)
    autoUpload(app, msg, path_download, bot.user_bot, msg.text.split(' ')[1])


# ------------------------------------------------------------------------- OPCIONES DEL ARCHIVO ⚙️
@bot.app.on_message(filters.regex("/op_") & filters.private)
def opcionesArchivo(app, msg):
    file = userFiles[msg.from_user.username][int(msg.text.split('_')[-1])]
    url = f"https://{bot.NAME_APP}.onrender.com/file/{msg.from_user.username}/{file}".replace(' ', '%20')
    # http://127.0.0.1:8000/file/KOD_16/
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton('⬆️ SUBIR ARCHIVO', callback_data=f'upload {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
    ])
    btn_url = InlineKeyboardMarkup([
        [InlineKeyboardButton('⬆️ SUBIR ARCHIVO', callback_data=f'upload {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🔗 ENLACE', url=url)],
    ])
    
    try:
        msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=btn_url)
    except Exception as e:
        print(e)
        msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=btn)




# ------------------------------------------------------------------------ RENOMBRAR ARCHIVO 📝
@bot.app.on_callback_query(filters.create(lambda f, c, u: "rename" in u.data))
def renombrarArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    callback.message.reply(f'**📝 Introduce el nuevo nombre para: `{basename(file)}`**', 
                          reply_markup=ForceReply(placeholder='Nuevo nombre'))


@bot.app.on_message(filters.reply & filters.private & filters.create(lambda f, c, u: u.reply_to_message.text.startswith('📝 Introduce el nuevo nombre para:')))
def cambiarNombre(app, msg):
    user = msg.from_user.username
    path_downloads = join('downloads', user)
    
    rename(join(path_downloads, msg.reply_to_message.text.split(': ')[-1]), 
           join(path_downloads, msg.text))
    
    msg.reply(f'**✅ Nombre cambiado a: `{msg.text}`**')
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
    if not message.from_user.username == 'MandiCoder':
        message.reply('Este bot solo lo puede usar su creador @MandiCoder 😛')
        return
    
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