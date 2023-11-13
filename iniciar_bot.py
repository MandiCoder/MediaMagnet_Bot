import subprocess
import time
import os

os.environ["BOT_TOKEN"] = '6393853527:AAGJp2_Yj_9sel4NC_rf0TzHuKxxVHjCPJs'
os.environ["DATABASE"] = 'mongodb://127.0.0.1'
os.environ["SESSION_STRING"] = 'AQFfwxsAEXP6WV1eL8byuyMrwe2zD863B-rvQKe3iCfrNH727f4HibYdcKKsKcmcRuv8pPLBh-chO0BqAUTjVbAkJccW2EKmVqTBb7E7zckdpsIhpgr9oCeYb_lZWCxeacMszqdXmQtWUEVKnZ0x6A5BrUa_GUuWlCqW2-Y3pkiWsgcNxvSfMW7v--R5yJ93DRRcIEhC2cGt23FyXcy8NwiZ-UIZghCI4XcmPGXEhPZkysMhB2K7CDok6alYE0NTflB8RFztAHu9NjWGIk6YBXACvBpf3CMiJRtUdMe7qc59A7trcTA9PNrr324itKGOCA2KNvMFB3mjeRGxHXs43jJX6bxXwwAAAABnQMmXAA'
os.environ["PORT"] = '8000'
os.environ["BOT_USER"] = 'KOD_16'
os.environ["API_HASH"] = 'ff9d2b13d574fd0206a14bd3ceac7502'
os.environ["BOT_TOKEN"] = '23053083'

comando = ['python3', 'main.py']
proceso = subprocess.Popen(comando)

while True:
    rd = input('Escriba (exit) para salir o presione enter para reiniciar el Bot: \n\n')
    if rd == 'exit':
        proceso.terminate()
        break
    else:
        print('\nReiniciando Bot...')
        proceso.terminate()
        time.sleep(5)
        proceso = subprocess.Popen(comando)
        
    
    
