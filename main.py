# MIS MODULOS
from modules.download_files_telegram import download_files_telegram
from modules.pyrogram_init import PyrogramInit
from modules.show_files import showFiles
from modules.download_files import downloadFiles
from modules.upload_files import uploadFile
from modules.database import create_db, update_db, read_db
from modules.generate_words import generateWord
from modules.auto_upload import autoUpload
from modules.extract_images import extractImages
from modules.global_variables import (btn_general, btn_opciones, userFiles, download_queues, download_queues_url, access_bot)
from modules.torrentp.torrent_downloader import TorrentDownloader
from modules.compress_files import compressFiles

# MODULOS EXTERNOS
from pickle import dump, load
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from os.path import join, basename, splitext, exists, isfile, isdir
from os import unlink, rename, listdir, makedirs
from queue import Queue as cola
from shutil import rmtree

bot = PyrogramInit()

@bot.app.on_message(filters.command('start'))
def enviar_mensajes(app, msg):
    create_db(msg.from_user.username)

    if not msg.from_user.username == 'MandiCoder':
        msg.reply('Hola, le doy la bienvenida a mi Bot')
        return
    else: 
        msg.reply('**Ola perra**', reply_markup=btn_general)
    

    
    
    
# ------------------------------------------------------------------------- VER ARCHIVOS DESCARGADOS
@bot.app.on_message(filters.regex('📁 Archivos'))
def mostrar_archivos(app, msg):
    username = msg.from_user.username
    file_path = join('archive', username, 'message.pkl')
    folder_path = join('archive', username)
    
    if not exists(folder_path):
        makedirs(folder_path)
        
    if exists(file_path):
        eliminarMensaje(username, msg.id)
    else:    
        msg.delete()
        
    sms = showFiles(msg, msg.from_user.username)
    
    with open(join(file_path), 'wb') as pk:
        dump(sms, pk)




# ------------------------------------------------------------------------- BORRAR TODOS LOS ARCHIVOS 🗑
@bot.app.on_callback_query(filters.create(lambda f, c, u: "borrar_todo" in u.data))
def borrarTodo(app, callback):
    path_downloads = join('downloads', callback.from_user.username)
    c = 0
    for c, i in enumerate(listdir(path_downloads)):
        c+=1
        path = join(path_downloads, i)
        if isdir(path):
            rmtree(path)
        else:
            unlink(path)
    callback.message.delete()
    callback.message.reply(f'**✅ {c} Archivos eliminados**')
    
    
    
    

# ------------------------------------------------------------------------- COMPRIMIR ARCHIVOS 📦
@bot.app.on_message(filters.regex('📦 Comprimir todo'))
def enviar_mensaje_comprimir(app, msg):
    eliminarMensaje(msg.from_user.username, msg.id)
    text = "**📝 Ingrese el nombre del archivo: \n🔐 Debajo una contraseña (Opcional)**"
    text += "**\n\nEjemplo: `\n    MiArchivoZip\n    MiContraseña`**"
    msg.reply(text, reply_markup=ForceReply(placeholder="Nombre del archivo:"))
    
@bot.app.on_message(filters.reply & filters.create(lambda f, c, u: u.reply_to_message.text.startswith('📝 Ingrese el nombre del archivo:')))
def recibir_mensaje_comprimir(app, msg):
    bot.app.delete_messages(msg.chat.id, (msg.id, msg.reply_to_message.id))
    username = msg.from_user.username
    user_path = join('downloads', username)
    list_files = []
    
    for i in listdir(user_path):
        full_path = join(user_path, i)
        if isfile(full_path):
            list_files.append(full_path)
    
    compressFiles(app, msg, list_files, msg.text, user_path)
    
    


# ------------------------------------------------------------------------- OPCIONES GENERALES ⚙️
@bot.app.on_message(filters.regex('⚙️ Opciones'))
def mostrar_opciones(app, msg):
    username = msg.from_user.username
    eliminarMensaje(username, msg.id)
    text = f'Zip size: `{read_db(username)["zip_size"]} MB`'
    sms = msg.reply(f'**⚙️ Opciones:\n\n {text}**', reply_markup=btn_opciones)
    guardarMensaje(username, sms)


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
@bot.app.on_message(filters.text & filters.create(lambda f, c, u: u.text.startswith('http')) |
                    filters.text & filters.create(lambda f, c, u: u.text.startswith('magnet:')) & 
                    filters.private)

def descargar_archivos_url(app, msg):
    username = msg.from_user.username
    
    if username not in access_bot:
        path_download = join('temp', username, generateWord(5))
        autoUpload(app, msg, path_download, msg.text) 
        
    else:
        path_user = join('downloads', username)
        if not exists(path_user): 
            makedirs(path_user)
        file_info = (app, msg.chat.id, msg.text, path_user)
        msg.reply("📌 __Enlace añadido a la cola__", quote=True)
        
        if username in download_queues_url:
            download_queues_url[username].put(file_info)
            
        else:
            queue = cola()
            queue.put(file_info)
            download_queues_url[username] = queue
            descargar_archivos(username)


def descargar_archivos(username):
    queue = download_queues_url[username]

    while not queue.empty():
        app, message_id, url, path_user = queue.get()
        try:
            downloadFiles(app, message_id, url, path_user, read_db(username)['video_quality'])
        except Exception as x:
            app.send_message(message_id, x)
        queue.task_done()

    del download_queues_url[username]

# ================================================ DESCARGAR ARCHIVOS EN CANALES
@bot.app.on_message(filters.command('dl'))
def descargarArchivosEnGrupos(app, msg):
    username = msg.from_user.username
    path_download = join('temp', username, generateWord(5))
    create_db(username)
    autoUpload(app, msg, path_download, msg.text.split(' ')[1])


# ------------------------------------------------------------------------- OPCIONES DEL ARCHIVO ⚙️
@bot.app.on_message(filters.regex("/op_") & filters.private)
def opcionesArchivo(app, msg):
    username = msg.from_user.username
    file = userFiles[username][int(msg.text.split('_')[-1])]
    url = f"https://{bot.NAME_APP}.onrender.com/file/{username}/{file}".replace(' ', '%20')
    # http://127.0.0.1:8000/file/KOD_16/
    
    if bot.NAME_APP is not None:
        url = f"https://{bot.NAME_APP}.onrender.com/file/{username}/{file}".replace(' ', '%20')
    else:
        url = f"http://127.0.0.1:8000/file/{file}".replace(' ', '%20')

    lista_botones = [
        [InlineKeyboardButton('⬆️ SUBIR ARCHIVO', callback_data=f'upload {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
        [InlineKeyboardButton('🔗 ENLACE', url=url)],
    ]
    
    if splitext(file)[1] in ('.mp4', 'mkv'):
        lista_botones.insert(2, [InlineKeyboardButton('🗂 EXTRAER IMAGENES', callback_data=f'extract_img {msg.text.split("_")[-1]}')])
        
    elif file.endswith(".torrent"):
        lista_botones = [
            [InlineKeyboardButton('🏴‍☠️ DESCARGAR TORRENT', callback_data=f'torrentdl {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR ARCHIVO', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        ]
    elif isdir(file):
        lista_botones = [
            [InlineKeyboardButton('📦 COMPRIMIR CARPETA', callback_data=f'compress_folder {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR CARPETA', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        ]
    
    eliminarMensaje(username, msg.id)
    try:
        msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=InlineKeyboardMarkup(lista_botones))
    except Exception as e:
        print(e)
        del lista_botones[-1]
        msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=InlineKeyboardMarkup(lista_botones))





# ------------------------------------------------------------------------ COMPRIMIR CARPETA 📦
@bot.app.on_callback_query(filters.create(lambda f, c, u: "compress_folder" in u.data))
def comprimirCarpeta(app, callback):
    username = callback.from_user.username
    folder = userFiles[username][int(callback.data.split(' ')[-1])]
    path_downloads = join('downloads', username)
    list_files = set()
    
    for file in listdir(folder):
        list_files.add(join(folder, file))
    
    callback.message.delete()
    compressFiles(app, callback.message, list_files, basename(folder), path_downloads)






# ------------------------------------------------------------------------ DESCARGAR ARCHIVO TORRENT 🏴‍☠️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "torrentdl" in u.data))
def descargarTorrent(app, callback):
    username = callback.from_user.username
    file = userFiles[username][int(callback.data.split(' ')[-1])]
    path_downloads = join('downloads', username)
    
    callback.message.delete()
    sms = callback.message.reply("**Descargando archivo torrent..**")
      
    torrent_file = TorrentDownloader(file, path_downloads, sms)
    torrent_file.start_download()




# ------------------------------------------------------------------------ RENOMBRAR ARCHIVO 📝
@bot.app.on_callback_query(filters.create(lambda f, c, u: "rename" in u.data))
def renombrarArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    callback.message.reply(f'**📝 Introduce el nuevo nombre para: `{basename(file)}`**', 
                          reply_markup=ForceReply(placeholder='Nuevo nombre'))


@bot.app.on_message(filters.reply & filters.private & filters.create(lambda f, c, u: u.reply_to_message.text.startswith('📝 Introduce el nuevo nombre para:')))
def cambiarNombre(app, msg):
    username = msg.from_user.username
    path_downloads = join('downloads', username)
    
    rename(join(path_downloads, msg.reply_to_message.text.split(': ')[-1]), 
           join(path_downloads, msg.text))
    
    msg.reply(f'**✅ Nombre cambiado a: `{msg.text}`**')
    sms = showFiles(msg, username)
    guardarMensaje(username, sms)


# ------------------------------------------------------------------------- SUBIR UN ARCHIVO ⬆️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "upload" in u.data))
def subirArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    uploadFile(app, callback.message, file, callback.from_user.username)






# ------------------------------------------------------------------------- SUBIR TODO 📤
@bot.app.on_message(filters.regex('📤 Subir todo') & filters.private)
def subirTodo(app, msg):
    username = msg.from_user.username
    eliminarMensaje(username, msg.id)
    path_downloads = join('downloads', username)
    msg.delete()
    sms = msg.reply(f'**📤 Subiendo {len(listdir(path_downloads))} Archivos**')

    for file in listdir(path_downloads):
        uploadFile(app, msg, join(path_downloads, file), username)
    sms.delete()





# ----------------------------------------------------------------------- EXTRAER IMAGENES 🗂
@bot.app.on_callback_query(filters.create(lambda f, c, u: "extract_img" in u.data))
def extraerImagenes(app, callback):
    user = callback.from_user.username
    file = userFiles[user][int(callback.data.split(' ')[-1])]
    extractImages(join('downloads', user, file), user)

    
    

# ---------------------------------------------------------------------- ELIMINAR UN ARCHIVO 🚮
@bot.app.on_callback_query(filters.create(lambda f, c, u: "del_file" in u.data))
def elimiarArchivo(app, callback):
    username = callback.from_user.username
    file = userFiles[username][int(callback.data.split(' ')[-1])]    
    
    if isfile(file):
        unlink(file)
    else:
        rmtree(file)    
    callback.message.edit(f'✅ {basename(file)} eliminado')
    
    sms = showFiles(callback.message, username)
    guardarMensaje(username, sms)



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


# ---------------------------------------------------------- MANEJAR MENSAJES
def eliminarMensaje(username:str, msg_id:int):
    file_path = join('archive', username, 'message.pkl')
    with open(file_path, 'rb') as pk:
        sms_pk = load(pk)
        bot.app.delete_messages(sms_pk.chat.id, (sms_pk.id, msg_id))


def guardarMensaje(username:str, sms:object):
    file_path = join('archive', username, 'message.pkl')
    
    with open(join(file_path), 'wb') as pk:
        dump(sms, pk)

if __name__ == '__main__':
    bot.iniciar_bot()