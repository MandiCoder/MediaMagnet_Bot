from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modules.ansi import green, purple
from subprocess import Popen
from time import sleep
from os import environ


environ["BOT_TOKEN"] = '6393853527:AAGJp2_Yj_9sel4NC_rf0TzHuKxxVHjCPJs'
environ["DATABASE"] = 'mongodb://127.0.0.1'
# environ["SESSION_STRING"] = ''
environ["PORT"] = '8000'
environ["BOT_USER"] = 'MandiCoder'
environ["API_HASH"] = 'ff9d2b13d574fd0206a14bd3ceac7502'
environ["API_ID"] = '23053083'

class eventHandler(FileSystemEventHandler):
    def __init__(self, proceso):
        super().__init__()
        self.proceso = proceso
    
    def on_modified(self, event):
        print(purple("\nReiniciando Bot..."))
        self.proceso.terminate()
        self.proceso = Popen(comando)

comando = ['python3', 'main.py']
proceso = Popen(comando)

observer = Observer()
observer.schedule(eventHandler(proceso), "./main.py", recursive=False)
observer.schedule(eventHandler(proceso), "./modules", recursive=True)
observer.start()

try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
    proceso.terminate()
observer.join()




# while True:
#     rd = input(green('Escriba (exit) para salir o presione Enter para reiniciar el Bot: \n\n'))
#     if rd == 'exit':
#         proceso.terminate()
#         break
#     else:
#         
#         proceso.terminate()
#         sleep(5)
#         
        
    
    
