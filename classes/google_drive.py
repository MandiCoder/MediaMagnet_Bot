from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from os.path import join
from time import localtime
import sys

class googleDrive():
    def __init__(self, message_telegram = None) -> None:
        self._credential_path = 'secret/credentials_module.json'
        self._drive = self.login()
        self._second = 0
        self.sms = message_telegram
        
        
    def login(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(self._credential_path)
        
        if gauth.access_token_expired:
            gauth.Refresh()
            gauth.SaveCredentialsFile(self._credential_path)
        else:
            gauth.Authorize()
        return GoogleDrive(gauth)
    
    
    
    def download(self, url, folder_path='./'):
        if 'folders' not in url: # DESCARGAR UN ARCHIVO
            file_id = url.split('/')[-2]
            self.downloadFile(file_id, folder_path)
        else: # DESCARGAR EL CONTENIDO DE UNA CARPETA
            if url.endswith('drive_link'):
                folder_id = url.split('/')[-1].split('?')[0]
            else:
                folder_id = url.split('/')[-1]
            
            file_list = self._drive.ListFile( {'q' : f"'{folder_id}' in parents and trashed=false"} ).GetList()
            for file in file_list:
                print('Descargando:', file['title'], )
                self.downloadFile(file['id'], folder_path)
                
                
                
    def downloadFile(self, file_id, folder_path):
        file = self._drive.CreateFile({'id': file_id})
        print("Descargando: ", file['title'])
        file.GetContentFile(filename=join(folder_path, file['title']), callback=self.progress_callback)
        
        
        
    def progress_callback(self, bytes_transferred, file_size):
        if self._second != localtime().tm_sec:
            try:
                self.sms.edit_text(f"bytes_transferred: {bytes_transferred}\nfile_size: {file_size}")
            except:
                pass
            self._second = localtime().tm_sec
        
        
        # percentage = (bytes_transferred / file_size) * 100
        # print(f"Descargado: {percentage}%", end='\r')
        # sys.stdout.flush()
            