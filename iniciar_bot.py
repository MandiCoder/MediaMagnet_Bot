from modules.ansi import green, purple
import subprocess
import time
import os

os.environ["BOT_TOKEN"] = '6393853527:AAGJp2_Yj_9sel4NC_rf0TzHuKxxVHjCPJs'
os.environ["DATABASE"] = 'mongodb://127.0.0.1'
# os.environ["SESSION_STRING"] = ''
os.environ["PORT"] = '8000'
os.environ["BOT_USER"] = 'MandiCoder'
os.environ["API_HASH"] = 'ff9d2b13d574fd0206a14bd3ceac7502'
os.environ["API_ID"] = '23053083'

comando = ['python3', 'main.py']
proceso = subprocess.Popen(comando)

while True:
    rd = input(green('Escriba (exit) para salir o presione Enter para reiniciar el Bot: \n\n'))
    if rd == 'exit':
        proceso.terminate()
        break
    else:
        print(purple("\nReiniciando Bot..."))
        proceso.terminate()
        time.sleep(5)
        proceso = subprocess.Popen(comando)
        
    
    
