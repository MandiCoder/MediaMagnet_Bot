from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modules.ansi import purple
from subprocess import Popen
from os import environ


environ["BOT_TOKEN"] = '6953816594:AAG-ECps_eDr4a38_xmTUZmrM_ONIRbNHh4'
environ["DATABASE"] = 'mongodb://127.0.0.1'
environ["SESSION_STRING"] = 'AQEjY1QAigM-3n_RXKS94gzOr_yYKbj1RZ6cO1gZVrU2H6zQHhxDKM7kE9jdYRLjGzSOOXmoDktwfTrKuPsC8WVzExiSAAIPmetYg0cWaMTnQtWzORvEmkz4uZyFxfUo4lM56HxvLun4O4Djmu7b7bswYekLNsPr2AYkN1CBlgjEoKfbT9yCul2lkh3FxL4HTIvF_62aWUaRDYZWkGLQkivTJrRzlg786K6LHFgLixAskOhfko3nqBiBxXM1A3HExEFtXYdhZhf2pWCZOY2rYl7TZT8JVaJ7UXrakgfDPiNTRg37k0hflbiyiE1poFMuiNMzYSapeQqPG7go8V0ubdklcfkp4AAAAABnQMmXAA'
environ["PORT"] = '8000'
environ["BOT_USER"] = 'MandiCoder'
environ["API_HASH"] = 'ff9d2b13d574fd0206a14bd3ceac7502'
environ["API_ID"] = '23053083'


class eventHandler(FileSystemEventHandler):
    def __init__(self, proceso):
        super().__init__()
        self.proceso = proceso
    
    def on_modified(self, event):
        if '__pycache__' not in event.src_path:
            print(purple("\nReiniciando Bot..."))
            self.proceso.terminate()
            self.proceso = Popen(comando)

comando = ['python3', 'main.py']
proceso = Popen(comando)

observer = Observer()
observer.schedule(eventHandler(proceso), "./main.py", recursive=False)
# observer.schedule(eventHandler(proceso), "./modules", recursive=True)
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
        
    
    
