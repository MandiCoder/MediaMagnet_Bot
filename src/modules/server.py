import jinja2
import aiohttp_jinja2
import os
from aiohttp import web
from aiohttp import streamer
from .show_files import sizeof

"""==============Envio de el Archivo por HTTP================="""

@streamer
async def file_sender(writer, file_path=None):
    with open(file_path, "rb") as f:
        chunk = f.read(2**16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2**16)

"""===============Servicio de Recepcion de la Peticion GET==================="""

async def download_file(request):
    file_name = request.match_info["file_name"]
    route = request.match_info["route"]
    file_path = os.path.join('downloads', route, file_name)
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(
            file_name=file_name
        ),
        "Accept-Ranges": "bytes",
        "Content-Type": f'{file_path.split("/")[-1].split(".")[-1]}',
        "Content-Length": str(os.path.getsize(file_path)),
    }

    if not os.path.exists(file_path):
        return web.Response(
            body="El Archivo  <{file_name}> No Existe".format(file_name=file_name),
            status=404,
        )

    return web.Response(body=file_sender(file_path=file_path), headers=headers)



async def index(request):
    file_path = "./templates/index.html"
    # Envio de Parametros al HTML
    nombre = "Rey"
    data = {"nombre": nombre, "estilos": "styles.css"}
    with open(file_path, "r") as file:
        template = jinja2.Template(file.read())
        html = template.render(data)
    return web.Response(text=html, content_type="text/html")


@aiohttp_jinja2.template('user.html')
async def list_files(request):
    user = request.match_info.get('user')
    path = f"downloads/{user}"
    archivos = []
    for file in os.listdir(path):
        path_file = os.path.join(path, file)
        if os.path.isfile(path_file):
            size = sizeof(os.path.getsize(path_file))
            archivos.append(
                {
                    'peso'   : size,
                    'ruta'   : path_file,
                    'nombre' : file,
                    'enlace' : os.path.join(os.getenv('HOST'), "files", path_file)
                }
            )
        
    return {
        'archivos': archivos,
        'usuario' : user
    }



async def video_handler(request):
    username = request.match_info["username"]
    file = request.match_info["file_name"]
    with open(os.path.join('downloads', username, file), 'rb') as f:
        video_data = f.read()
    headers = {'Content-Type': 'video/mp4'}
    return web.Response(body=video_data, headers=headers)