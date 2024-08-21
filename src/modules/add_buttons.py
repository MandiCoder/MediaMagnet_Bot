from pyrogram.types import InlineKeyboardButton
from os.path import splitext, isdir, basename
from os import getenv
from magic import Magic

HOST=getenv("HOST")

def addButtons(file:str, msg:object, username:str):
    url = f"{HOST}/file/downloads/{username}/{basename(file)}".replace(' ', '%20')
    url_video = f"{HOST}/video/downloads/{username}/{basename(file)}".replace(' ', '%20')
    
    m = Magic()
    type = m.from_file(file)
    
    lista_botones = [
            [InlineKeyboardButton('⬆️ SUBIR A TELEGRAM', callback_data=f'upload {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('☁️ SUBIR A GOOGLE DRIVE', callback_data=f'upload_drive {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🔗 ENLACE', url=url_video)],
        ]
    
    
    if splitext(file)[1] in ('.mp4', 'mkv'):
        lista_botones.append(
            [InlineKeyboardButton('🗂 EXTRAER IMAGENES', callback_data=f'extract_img {msg.text.split("_")[-1]}')],
        )
        

    elif file.endswith(".torrent"):
        lista_botones = [
            [InlineKeyboardButton('🏴‍☠️ DESCARGAR', callback_data=f'torrentdl {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        ]
        
    elif isdir(file):
        lista_botones = [
            [InlineKeyboardButton('📂 ABRIR', callback_data=f'open_folder {msg.text.split("_")[-1]}'),
             InlineKeyboardButton('📦 SUBIR', callback_data=f'compress_folder {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}'),
             InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],          
        ]
        
    return lista_botones