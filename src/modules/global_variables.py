from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# DICCIONARIOS GLOBALES
userFiles = {}
download_queues = {}
download_queues_url = {}
user_path = {}

progreso_usuarios = {}
detener_progreso = {}

# BOTONES
btn_general = ReplyKeyboardMarkup([
        ['⚙️ Opciones'],
        ['📤 Subir todo', '📦 Comprimir todo'],
    ], resize_keyboard=True, one_time_keyboard=True)

btn_opciones = InlineKeyboardMarkup([
        [InlineKeyboardButton('📚 ZIP SIZE', callback_data='zip_size')]
    ])

# ACCESO AL BOT
access_bot = (
    'MandiCoder'
)

