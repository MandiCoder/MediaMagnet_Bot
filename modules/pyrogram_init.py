from pyrogram.methods.utilities.idle import idle
from modules.ansi import green
from .server import index
from pyrogram import Client
from aiohttp import ClientSession
from asyncio import sleep as asyncsleep
from aiohttp import web
from os import getenv

from modules.server import download_file

class PyrogramInit():
    def __init__(self, 
                 PORT=getenv("PORT"), 
                 NAME_APP=getenv("NAME_APP"),
                 API_HASH=getenv("API_HASH"),
                 API_ID=getenv("API_ID"),
                 BOT_TOKEN=getenv("BOT_TOKEN"),
                 SESSION_STRING=getenv("SESSION_STRING")):
        
        self.PORT = PORT
        self.NAME_APP = NAME_APP
        self.API_HASH = API_HASH
        self.API_ID = API_ID
        self.BOT_TOKEN = BOT_TOKEN
        self.SESSION_STRING = SESSION_STRING
        self.app = Client(name='TelegramBot', api_hash=self.API_HASH, api_id=self.API_ID, bot_token=self.BOT_TOKEN)
        self.user_bot = Client("UserBot", api_id=self.API_ID, api_hash=self.API_HASH, bot_token=self.BOT_TOKEN, session_string=self.SESSION_STRING)
        
    def iniciar_bot(self):
        print(green("INICIANDO BOT"))
        self.app.loop.run_until_complete(self.run_server())
        self.app.loop.run_until_complete(self.despertar())
        idle()

    async def despertar(self, sleep_time=10 * 60):
        while True:
            await asyncsleep(sleep_time)
            async with ClientSession() as session:
                async with session.get(f'https://{self.NAME_APP}.onrender.com/' + "/Despiertate"):
                    pass
    
    async def run_server(self):
        server = web.Application()
        server.router.add_get("/file/{route}/{file_name}", download_file)
        server.router.add_get("/", index)
        runner = web.AppRunner(server)
        
        await self.app.start()
        print(green('BOT INICIADO'))
        
        await self.user_bot.start()
        print(green('USER-BOT INICIADO'))
        
        await runner.setup()
        await web.TCPSite(runner, host='0.0.0.0', port=self.PORT).start()
        print(green('SERVER INICIADO'))
    