from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from os.path import join
from time import localtime
import sys



settings = {
    'client_config_backend': 'settings',
    'client_config':{
        'client_id': '404427750734-aq6gsb6rli0rn9aarlac2r2d1j9qc1h3.apps.googleusercontent.com',
        'client_secret': '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'
    },
    'save_credentials': True,
    'save_credentials_backend': 'file',
    'save_credentials_file': 'credentials_module.json',
    'get_refresh_token': True,
    'oauth_scope':['https://www.googleapis.com/auth/drive']
}



class googleDrive():
    def __init__(self, message_telegram = None) -> None:
        self._credential_path = 'secret/credentials_module.json'
        self._second = 0
        self.sms = message_telegram
        self.gauth = GoogleAuth(settings=settings)
        self.folder_id = '1PNry1hw6iLsyWBEKkbXBhnhkPMPKccOM'
        self.drive = self.login()
        
        
        
    def login(self):
        self.gauth.LoadCredentialsFile(self._credential_path)
        if self.gauth.access_token_expired:
            self.gauth.Refresh()
            self.gauth.SaveCredentialsFile(self._credential_path)
        else:
            self.gauth.Authorize()
        return GoogleDrive(self.gauth)
    
    
    
    def login_browser(self):
        self.gauth.LocalWebserverAuth()
        
        
        
    def ver_archivos(self):
        file_list = self.drive.ListFile({'q': f"'{self.folder_id}' in parents and trashed=false"}).GetList()
        data = []
        for file in file_list:
            download_url = file['webContentLink']
            title = file['title']
            file_size = file['fileSize']
            data.append(
                {
                    "download_url" : download_url,
                    "title"        : title,
                    "file_size"    : self.sizeof(int(file_size))
                }
            )
        return data


    def sizeof(self, num: int, suffix="B"):
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, "Yi", suffix)
    
    
    def download(self, url, folder_path='./'):
        if 'folders' not in url: # DESCARGAR UN ARCHIVO
            file_id = url.split('/')[-2]
            self.downloadFile(file_id, folder_path)
        else: # DESCARGAR EL CONTENIDO DE UNA CARPETA
            if url.endswith('drive_link'):
                folder_id = url.split('/')[-1].split('?')[0]
            else:
                folder_id = url.split('/')[-1]
            
            file_list = self.drive.ListFile( {'q' : f"'{folder_id}' in parents and trashed=false"} ).GetList()
            for file in file_list:
                print('Descargando:', file['title'], )
                self.downloadFile(file['id'], folder_path)
                
                
                
    def subir_archivo(self, filename:str):
        """
        La función "subir_archivo" sube un archivo a Google Drive.
        
        :param filename: El nombre del archivo que deseas cargar en Google Drive.
        :param drive: Una instancia de GoogleDrive para interactuar con la API.
        :param folder_id: (Opcional) El ID de la carpeta donde se subirá el archivo. Si no se proporciona, se subirá a la raíz de Google Drive.
        """
        file = self.drive.CreateFile({'parents': [{'id': self.folder_id}]})
        file.SetContentFile(filename)
        file.Upload()
        file.FetchMetadata(fields='webContentLink, webViewLink')
        return file['webContentLink']
               
               
                
    def eliminar_archivo(self, filename:str):
        pass
                
                
                
    def downloadFile(self, file_id, folder_path):
        file = self.drive.CreateFile({'id': file_id})
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
            
