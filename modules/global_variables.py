from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .google_drive import login

# DICCIONARIOS GLOBALES
userFiles = {}
download_queues = {}
download_queues_url = {}

# BOTONES
btn_general = ReplyKeyboardMarkup([
        ['📁 Archivos', '⚙️ Opciones'],
        ['📤 Subir todo', '🗂 Subir album'],
    ], resize_keyboard=True, one_time_keyboard=True)

btn_opciones = InlineKeyboardMarkup([
        [InlineKeyboardButton('📚 ZIP SIZE', callback_data='zip_size')]
    ])

# ACCESO AL BOT
access_bot = (
    'MandiCoder'
)

drive = login()