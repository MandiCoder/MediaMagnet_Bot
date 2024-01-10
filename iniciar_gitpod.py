from subprocess import Popen
import subprocess
from os import environ

environ["BOT_TOKEN"] = '6953816594:AAG-ECps_eDr4a38_xmTUZmrM_ONIRbNHh4'
environ["DATABASE"] = 'mongodb://127.0.0.1'
# environ["SESSION_STRING"] = ''
environ["PORT"] = '8000'
environ["BOT_USER"] = 'MandiCoder'
environ["API_HASH"] = 'ff9d2b13d574fd0206a14bd3ceac7502'
environ["API_ID"] = '23053083'

comando_iniciar = ['python3', 'main.py']

Popen(comando_iniciar)