# MIS MODULOS
from src.modules.download_files_telegram import download_files_telegram
from src.modules.pyrogram_init import PyrogramInit
from src.modules.show_files import showFiles
from src.modules.download_files import downloadFiles
from src.modules.upload_files import uploadFile
from src.modules.database import create_db, update_db, read_db
from src.modules.auto_upload import autoUpload
from src.modules.extract_images import extractImages
from src.modules.torrentp.torrent_downloader import TorrentDownloader
from src.modules.compress_files import compressFiles
from src.modules.add_buttons import addButtons
from src.classes.google_drive import googleDrive
from src.modules.global_variables import (btn_general, btn_opciones, userFiles, 
                                      download_queues, download_queues_url,
                                      user_path, progreso_usuarios)
# MODULOS EXTERNOS
from pickle import dump, load
from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, ForceReply, InlineKeyboardButton)
from os.path import join, basename, exists, isfile, isdir, dirname
from os import unlink, rename, listdir, makedirs
from queue import Queue as cola
from shutil import rmtree

bot = PyrogramInit()



@bot.app.on_message(filters.command('start'))
def enviar_mensajes(app, msg):
    create_db(msg.from_user.username)
    msg.reply(f'**Hola {msg.from_user.username}, le doy la bienvenida a mi Bot**', reply_markup=btn_general)

    
    
    
#! ------------------------------------------------------------------------- VER ARCHIVOS 📁 
@bot.app.on_message(filters.command("files"))
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
        
    sms = showFiles(msg, username, user_path)
    
    with open(join(file_path), 'wb') as pk:
        dump(sms, pk)




#! ------------------------------------------------------------------------- VER ARCHIVOS EN DRIVE 📁 
@bot.app.on_message(filters.command("drive"))
def list_files(app, msg):
    sms = msg.reply("⏱** Procesando**", disable_web_page_preview=True)
    drive = googleDrive()
    files = drive.ver_archivos()
    about = drive.drive.GetAbout()

    total_quota = int(about['quotaBytesTotal'])
    used_quota = int(about['quotaBytesUsed'])
    free_quota = total_quota - used_quota
    
    txt = "☁️** Archivos en la nube: **\n"
    for count, file in enumerate(files):
        txt += f"**__[{file['title']}]({file['download_url']})__ | {file['file_size']}\n**"
        txt += f"**  ➥ /rm_{count}\n\n**"
    txt += "\n︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵\n"
    txt += f"**➤ Espacio total: --__{total_quota/1024**3:.2f} GB__--**\n"
    txt += f"**➤ Espacio usado: --__{used_quota/1024**3:.2f} GB__--**\n"
    txt += f"**➤ Espacio libre: --__{free_quota/1024**3:.2f} GB__--**\n"
    sms.edit_text(txt, disable_web_page_preview=True)


@bot.app.on_message(filters.create(lambda f, c, u: u.text.startswith('/rm_')))
def borrar_drive(app, msg):
    print(msg.text)


#! ------------------------------------------------------------------------- BORRAR TODOS LOS ARCHIVOS 🗑
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
    
    

#! ------------------------------------------------------------------------- SUBIR TODOS LOS ARCHIVOS A GOOGLE DRIVE ☁️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "subir_drive" in u.data))
def subirTodoDrive(app, callback):
    username = callback.from_user.username
    eliminarMensaje(username, callback.message.id)
    text = "**☁️ Subiendo archivos a GoogleDrive...**\n"

    sms = callback.message.reply(text)
    drive = googleDrive()
    if username not in user_path:
        path_downloads = join('downloads', username)
    else:
        path_downloads = user_path[username]

    for file in listdir(path_downloads):
        path = join(path_downloads, file)
        url = drive.subir_archivo(path)
        text += f"\n✅**[{file}]({url})**"
        sms.edit_text(text, disable_web_page_preview=True)

    

#! ------------------------------------------------------------------------- COMPRIMIR ARCHIVOS 📦
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
    
    if username not in user_path:
        path = join('downloads', username)
    else:
        path = user_path[username]
        
    list_files = []
    
    for i in listdir(path):
        full_path = join(path, i)
        if isfile(full_path):
            list_files.append(full_path)
    
    compressFiles(app, msg, list_files, msg.text, path)
    
    


#! ------------------------------------------------------------------------- OPCIONES GENERALES ⚙️
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
    

#! ---------------------------------------------------------------------- DESCARGAR DE ENLACES
@bot.app.on_message(filters.text & filters.create(lambda f, c, u: u.text.startswith('http')) |
                    filters.text & filters.create(lambda f, c, u: u.text.startswith('magnet:')) & 
                    filters.private)

def descargar_archivos_url(app, msg):
    username = msg.from_user.username
    
    # if username not in access_bot:
    #     autoUpload(app, msg, msg.text, bot.user_bot) 
        
    # else:

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
            downloadFiles(app, message_id, url, path_user, read_db(username)['video_quality'], bot.user_bot)
        except Exception as x:
            app.send_message(message_id, x)
        queue.task_done()

    del download_queues_url[username]

#! ================================================ DESCARGAR ARCHIVOS EN CANALES
@bot.app.on_message(filters.command('dl'))
def descargarArchivosEnGrupos(app, msg):
    username = msg.from_user.username
    create_db(username)
    autoUpload(app, msg, msg.text.split(' ')[1])




#! ------------------------------------------------------------------------- OPCIONES DEL ARCHIVO ⚙️
@bot.app.on_message(filters.regex("/op_") & filters.private)
def opcionesArchivo(app, msg):
    username = msg.from_user.username
    file = userFiles[username][int(msg.text.split('_')[-1])]
    eliminarMensaje(username, msg.id)
    msg.reply(f'**MAS OPCIONES PARA: `{basename(file)}`**', reply_markup=InlineKeyboardMarkup(addButtons(file, msg, username)))




#! ------------------------------------------------------------------------ AGREGAR THUMB 🌄
@bot.app.on_callback_query(filters.create(lambda f, c, u: "add_thumb" in u.data)) 
def agregarThumb(app, callback):
    pass
    
    
    
    
    
#! ------------------------------------------------------------------------ SUBIR A DRIVE ☁️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "upload_drive" in u.data))
def subirGoogleDrive(app, callback):
    sms = callback.message
    sms.edit_text("**🚀 Subiendo a GoogleDrive ☁️**")
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    drive = googleDrive()
    url = drive.subir_archivo(file)
    sms.edit_text(f"**✅ {basename(file)}**", reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔗 DESCARGAR", url=url)]
        ]
    ))
    
    
    
#! ------------------------------------------------------------------------ ABRIR CARPETA 📂
@bot.app.on_callback_query(filters.create(lambda f, c, u: "open_folder" in u.data))
def abrirCarpeta(app, callback):
    global user_path
    username = callback.from_user.username
    folder = userFiles[username][int(callback.data.split(' ')[-1])]
    user_path[username] = folder
    callback.message.delete()
    showFiles(callback.message, username, user_path)



#! ------------------------------------------------------------------------ IR ATRAS ⬅️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "atras" in u.data))
def volverAtras(app, callback):
    global user_path
    username = callback.from_user.username
    user_path[username] = dirname(user_path[username])
    callback.message.delete()
    showFiles(callback.message, username, user_path)




#! ------------------------------------------------------------------------ COMPRIMIR CARPETA 📦
@bot.app.on_callback_query(filters.create(lambda f, c, u: "compress_folder" in u.data))
def comprimirCarpeta(app, callback):
    username = callback.from_user.username
    folder = userFiles[username][int(callback.data.split(' ')[-1])]
    
    
    if username not in user_path:
        path = join('downloads', username)
    else:
        path = user_path[username]
        
    list_files = set()
    
    for file in listdir(folder):
        list_files.add(join(folder, file))
    
    callback.message.delete()
    file = compressFiles(app, callback.message, list_files, basename(folder), path, True)
    uploadFile(app, callback.message, file, username)
    unlink(file)



#! ------------------------------------------------------------------------ DESCARGAR ARCHIVO TORRENT 🏴‍☠️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "torrentdl" in u.data))
def descargarTorrent(app, callback):
    username = callback.from_user.username
    file = userFiles[username][int(callback.data.split(' ')[-1])]
    path_downloads = join('downloads', username)
    
    callback.message.delete()
    sms = callback.message.reply("**Descargando archivo torrent..**")
      
    torrent_file = TorrentDownloader(file, path_downloads, sms)
    torrent_file.start_download()




#! ------------------------------------------------------------------------ RENOMBRAR ARCHIVO 📝
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
    sms = showFiles(msg, username, user_path)
    guardarMensaje(username, sms)


#! ------------------------------------------------------------------------- SUBIR UN ARCHIVO ⬆️
@bot.app.on_callback_query(filters.create(lambda f, c, u: "upload" in u.data))
def subirArchivo(app, callback):
    file = userFiles[callback.from_user.username][int(callback.data.split(' ')[-1])]
    callback.message.delete()
    uploadFile(app, callback.message, file, callback.from_user.username)






#! ------------------------------------------------------------------------- SUBIR TODO 📤
@bot.app.on_message(filters.regex('📤 Subir todo') & filters.private)
def subirTodo(app, msg):
    username = msg.from_user.username
    eliminarMensaje(username, msg.id)
    if username not in user_path:
        path_downloads = join('downloads', username)
    else:
        path_downloads = user_path[username]
    
    msg.delete()
    sms = msg.reply(f'**📤 Subiendo {len(listdir(path_downloads))} Archivos**')

    for file in listdir(path_downloads):
        uploadFile(app, msg, join(path_downloads, file), username)
    sms.delete()





#! ----------------------------------------------------------------------- EXTRAER IMAGENES 🗂
@bot.app.on_callback_query(filters.create(lambda f, c, u: "extract_img" in u.data))
def extraerImagenes(app, callback):
    user = callback.from_user.username
    file = userFiles[user][int(callback.data.split(' ')[-1])]
    extractImages(join('downloads', user, file), user)

    
    

#! ---------------------------------------------------------------------- ELIMINAR UN ARCHIVO 🚮
@bot.app.on_callback_query(filters.create(lambda f, c, u: "del_file" in u.data))
def elimiarArchivo(app, callback):
    username = callback.from_user.username
    file = userFiles[username][int(callback.data.split(' ')[-1])]    
    
    if isfile(file):
        unlink(file)
    else:
        rmtree(file)    
    callback.message.edit(f'✅ {basename(file)} eliminado')
    
    sms = showFiles(callback.message, username, user_path)
    guardarMensaje(username, sms)



#! ---------------------------------------------------------------------- DESCARGAR ARCHIVOS DE TELEGRAM
@bot.app.on_message(filters.media & filters.private)
def descargarArchivosTelegram(app, message):
    # if not message.from_user.username == 'MandiCoder':
    #     message.reply('Este bot solo lo puede usar su creador @MandiCoder 😛')
    #     return
    
    username = message.from_user.username
    
    if username not in user_path:
        user_path[username] = join('downloads', username)

    if username in download_queues:
        download_queues[username].put( (message, user_path[username]) )
    else:
        queue = cola()
        queue.put( (message, user_path[username]) )
        download_queues[username] = queue
        download_files_telegram(app, username)
        
    # eliminarMensaje(username, message.id)


#! ---------------------------------------------------------- MANEJAR MENSAJES
def eliminarMensaje(username:str, msg_id:int):
    file_path = join('archive', username, 'message.pkl')
    with open(file_path, 'rb') as pk:
        sms_pk = load(pk)
        bot.app.delete_messages(sms_pk.chat.id, (sms_pk.id, msg_id))


def guardarMensaje(username:str, sms:object):
    file_path = join('archive', username, 'message.pkl')
    
    with open(join(file_path), 'wb') as pk:
        dump(sms, pk)
        

@bot.app.on_callback_query()
def enviar_mensaje(app, callback):
    msg = callback.message
    username:str = callback.from_user.username
    
    if callback.data == "compress":
        msg.reply_text("**🏷 Introduzca el nombre para el archivo:**", 
                    reply_markup=ForceReply(placeholder="Nombre:"))
        msg.delete()

    
    elif callback.data == "progress":
        callback.answer(progreso_usuarios[username], show_alert=True)


    # elif callback.data == "cancel_progreso":
    #     msg.delete()
    #     detener_progreso[username] = True
    #     show_data(msg, username)  

if __name__ == '__main__':
    bot.iniciar_bot()