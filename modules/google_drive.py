from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from os.path import join

ruta_credenciales = 'secret/credentials_module.json'

######################################################################################################## INICIAR SESION
def login():
    """
    La función `iniciar sesión` carga las credenciales de Google Drive, actualiza el token de acceso si
    ha caducado y autoriza el acceso a Google Drive.
    :return: una instancia de la clase GoogleDrive, que se inicializa con el objeto GoogleAuth.
    """
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(ruta_credenciales)
    
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(ruta_credenciales)
    else:
        gauth.Authorize()
        
    return GoogleDrive(gauth)

def downloadgd(url, folder_path='./'):
    """
    La función `descargarArchivo` toma una URL como entrada, extrae la ID del archivo de la URL, crea un
    objeto de archivo usando la ID del archivo y luego descarga el contenido del archivo y lo guarda con
    el título del archivo.
    
    :param url: El parámetro `url` es la URL del archivo que desea descargar
    """
    
    drive = login()
    if 'folders' not in url: # DESCARGAR UN ARCHIVO
        file_id = url.split('/')[-2]
        downloadFile(file_id, drive, folder_path)
    else: # DESCARGAR EL CONTENIDO DE UNA CARPETA
        if url.endswith('drive_link'):
            folder_id = url.split('/')[-1].split('?')[0]
        else:
            folder_id = url.split('/')[-1]
        
      
        file_list = drive.ListFile( {'q' : f"'{folder_id}' in parents and trashed=false"} ).GetList()
        for file in file_list:
            print('Descargando:', file['title'], )
            downloadFile(file['id'], drive, folder_path)
    
    

    
def downloadFile(file_id, drive, folder_path):
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(filename=join(folder_path, file['title']))