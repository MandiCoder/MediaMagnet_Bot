from pyrogram.methods.utilities.idle import idle
from src.modules.ansi import green, red, purple
from src.modules.server import download_file, video_handler
from .server import index
from pyrogram import Client
from aiohttp import ClientSession
from asyncio import sleep as asyncsleep
from aiohttp import web
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class PyrogramInit():
    def __init__(self, 
                 PORT=getenv("PORT"), 
                 HOST=getenv("HOST"),
                 API_HASH=getenv("API_HASH"),
                 API_ID=getenv("API_ID"),
                 BOT_TOKEN=getenv("BOT_TOKEN"),
                 SESSION_STRING=getenv("SESSION_STRING")):
        
        self.PORT = PORT
        self.HOST = HOST
        self.API_HASH = API_HASH
        self.API_ID = API_ID
        self.BOT_TOKEN = BOT_TOKEN
        self.SESSION_STRING = SESSION_STRING
        self.app = Client(name='TelegramBot', api_hash=self.API_HASH, api_id=self.API_ID, bot_token=self.BOT_TOKEN)
        self.user_bot = Client("UserBot", api_id=self.API_ID, api_hash=self.API_HASH, bot_token=self.BOT_TOKEN, session_string=self.SESSION_STRING)
        
        
    def iniciar_bot(self):
        print(green("INICIANDO BOT"))
        self.app.loop.run_until_complete(self.run_server())
        # self.app.loop.run_until_complete(self.despertar())
        idle()


    async def despertar(self, sleep_time=10 * 60):
        while True:
            await asyncsleep(sleep_time)
            async with ClientSession() as session:
                async with session.get(self.HOST + "/Despiertate"):
                    pass
    
    
    
    async def run_server(self):
        server = web.Application()
        server.router.add_get("/file/downloads/{route}/{file_name}", download_file)
        server.router.add_get("/", index)
        server.router.add_get("/video/downloads/{username}/{file_name}", video_handler)
        runner = web.AppRunner(server)
        
        await self.app.start()
        print(green('● BOT INICIADO'))
        
        try:
            await self.user_bot.start()
        except Exception as x:
            print(x)
        print(purple('● USER-BOT INICIADO'))
        
        await runner.setup()
        await web.TCPSite(runner, host='0.0.0.0', port=self.PORT).start()
        print(red('● SERVER INICIADO'))
    