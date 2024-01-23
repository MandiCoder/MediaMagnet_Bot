from pyrogram.types import InlineKeyboardButton
from os.path import splitext, isdir
from os import getenv

HOST=getenv("HOST")

def addButtons(file:str, msg:object, username:str):
    url = f"{HOST}/file/{file}".replace(' ', '%20')
    
    if splitext(file)[1] in ('.mp4', 'mkv'):
        lista_botones = [
            [InlineKeyboardButton('⬆️ SUBIR', callback_data=f'upload {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🗂 EXTRAER IMAGENES', callback_data=f'extract_img {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
        ]

    elif file.endswith(".torrent"):
        lista_botones = [
            [InlineKeyboardButton('🏴‍☠️ DESCARGAR', callback_data=f'torrentdl {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],
        ]
        
    elif isdir(file):
        lista_botones = [
            [InlineKeyboardButton('📂 ABRIR', callback_data=f'open_folder {msg.text.split("_")[-1]}'),
             InlineKeyboardButton('📦 COMPRIMIR', callback_data=f'compress_folder {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}'),
             InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],          
        ]
        
    else:
        lista_botones = [
            [InlineKeyboardButton('⬆️ SUBIR', callback_data=f'upload {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('📝 CAMBIAR NOMBRE', callback_data=f'rename {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🚮 ELIMINAR', callback_data=f'del_file {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🌄 AGREGAR IMAGEN', callback_data=f'add_thumb {msg.text.split("_")[-1]}')],
            [InlineKeyboardButton('🔗 ENLACE', url=url)],
        ]
        
    return lista_botones