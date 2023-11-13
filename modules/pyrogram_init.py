from pyrogram.methods.utilities.idle import idle
from pyrogram import Client, filters
from aiohttp import ClientSession
from asyncio import sleep as asyncsleep
from aiohttp import web
from os import getenv

from modules.server import download_file

class PyrogramInit():
    def __init__(self, 
                 PORT=getenv('PORT'), 
                 NAME_APP=getenv("NAME_APP"),
                 API_HASH=getenv("API_HASH"),
                 API_ID=getenv("API_ID"),
                 BOT_TOKEN=getenv("BOT_TOKEN")):
        
        self.PORT = PORT
        self.NAME_APP = NAME_APP
        self.API_HASH = API_HASH
        self.API_ID = API_ID
        self.BOT_TOKEN = BOT_TOKEN
        self.app = Client(name='TelegramBot', api_hash=self.API_HASH, api_id=self.API_ID, bot_token=self.BOT_TOKEN)
        
    def iniciar_bot(self):
        print("INICIANDO BOT")
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
        runner = web.AppRunner(server)
        
        await self.app.start()
        print('BOT INICIADO')
        
        await runner.setup()
        await web.TCPSite(runner, host='0.0.0.0', port=self.PORT).start()
        print('SERVER INICIADO')
    