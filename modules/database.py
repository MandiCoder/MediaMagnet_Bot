from json import dump, load
from os.path import join, exists

def create_db(username:str):        
    data = {
        'username'  :   username,
        'zip_size' :   2000,
    }
    
    if not exists(join('db', f'{username}.json')):
        with open(join('db', f'{username}.json'), "w") as f:
            dump(data, f)
            
            
            
def read_db(username:str) -> dict:
    """
    La función `read_db` lee un archivo JSON de una carpeta de base de datos según el nombre de usuario
    proporcionado y devuelve los datos como un diccionario.
    
    :param username: El parámetro `username` es una cadena que representa el nombre de usuario del
    usuario cuya base de datos desea leer
    :type username: str
    :return: un diccionario que contiene los datos leídos del archivo JSON asociado con el nombre de
    usuario dado.
    """
    
    with open(join('db', f'{username}.json'), "r") as f:
        data = load(f)
        return data
    
    
    
def update_db(username:str, clave:str, valor:str):
    """ 
    Parametros:
    `clave:` zip_size
    """
    with open(join('db', f'{username}.json'), "r") as f:
        data = load(f)
        data[clave] = valor
        
    with open(join('db', f'{username}.json'), "w") as f:
            dump(data, f)