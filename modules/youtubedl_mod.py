import unicodedata
import random
import re

# Apps de Terceros
import yt_dlp
import subprocess
import os


"""==================Modificacion de Texto======================="""
import unicodedata
import random
import re

# Apps de Terceros
import yt_dlp


class YoutubeDL:
    def __init__(self, downlad_progres=None, msg=None, bot=None, isTwitch=False):
        self.downlad_progres = downlad_progres
        self.msg = msg
        self._isTwitch = isTwitch
        self.bot = bot

    """============Conversion de Nombres============="""

    def slugify(self, value, allow_unicode=False):
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        ext = str(value).split(".")[-1]
        value = str(value).split(".")[0]
        if allow_unicode:
            value = unicodedata.normalize("NFKC", value)
        else:
            value = (
                unicodedata.normalize("NFKD", value)
                .encode("ascii", "ignore")
                .decode("ascii")
            )
        value = re.sub(r"[^\w\s-]", "", value.lower())
        return re.sub(r"[-\s]+", "-", value).strip("-_")

    """==================Progreso de Descarga de Videos==================="""

    def my_hook(self, d):
        if d["status"] == "downloading":
            if not self._isTwitch:
                filename = d["filename"]
                current = d["downloaded_bytes"]
                total = d["total_bytes"]
                speed = 0
                if d["speed"] is not None:
                    speed = d["speed"]
                tiempo = d["_eta_str"]
                self.downlad_progres(
                    int(current),
                    int(total),
                    speed,
                    filename,
                    tiempo,
                    self.msg,
                    self.bot,
                )
            else:
                filename = d["filename"]
                current = d["downloaded_bytes"]
                speed = 0
                if d["speed"] is not None:
                    speed = d["speed"]
                tiempo = d["_eta_str"]
                self.downlad_progres(
                    int(current), speed, filename, tiempo, self.msg, self.bot
                )
        if d["status"] == "finished":
            print("Done downloading, now converting ...")

    """==================INFORMACION DEL VIDEO==================="""

    def metaInfo(self, url):
        ydl_opts = {"restrict_filenames": True, "windowsfilenames": False}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)

        dicTitle = {}

        if "thumbnails" in meta.keys():
            dicTitle["Thumb"] = meta["thumbnails"][-1]["url"]
        if "fulltitle" in meta.keys():
            dicTitle["Title"] = meta["fulltitle"]

        return dicTitle

    """==================Informacion de el Video==================="""

    def info(self, url):
        ydl_opts = {"restrict_filenames": True, "windowsfilenames": False}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)

        formats = meta["formats"]

        id = []
        ext = []
        formato = []
        FILESIZE = []
        for format in formats:
            if "youtu" in url:
                if format['vcodec'] != 'none' and format['acodec'] != 'none':
                    try:
                        if "filesize_approx" in format.keys():
                            SIZE = round(format["filesize_approx"] / 1e6, 2)
                        elif "filesize" in format.keys():
                            SIZE = round(format["filesize"] // 1e6, 2)
                        else:
                            SIZE = 0
                        if SIZE > 1000:
                            SIZE = SIZE // 1000
                            SIZE = str(SIZE) + " GB"
                        else:
                            SIZE = str(SIZE) + " MB"
                        FILESIZE.append(SIZE)
                    except Exception as e:
                        print(e)
                        FILESIZE.append("No Disponible")
                        
                    id.append(format["format_id"])
                    ext.append(format["ext"])
                    formato.append(format["format"].split(sep="-")[-1])

            else:
                if "mhtml" not in format["ext"] and "ultralow" not in format["format"]:
                    try:
                        if "filesize_approx" in format.keys():
                            SIZE = round(format["filesize_approx"] / 1e6, 2)
                        elif "filesize" in format.keys():
                            SIZE = round(format["filesize"] // 1e6, 2)
                        else:
                            SIZE = 0
                        if SIZE > 1000:
                            SIZE = SIZE // 1000
                            SIZE = str(SIZE) + " GB"
                        else:
                            SIZE = str(SIZE) + " MB"
                        FILESIZE.append(SIZE)
                    except Exception as e:
                        print(e)
                        FILESIZE.append("No Disponible")
                    id.append(format["format_id"])
                    ext.append(format["ext"])
                    formato.append(format["format"].split(sep="-")[-1])
        guardar = []
        for val1, val2, val3, val4 in zip(id, ext, formato, FILESIZE):
            guardar.append(val1 + ":" + val3 + ":" + val2 + ":" + val4)

        return guardar

    """================Obtencion del Titulo del Video================"""

    def getTitle(self, url):
        elem = "abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ids = "".join(random.sample(elem, 4))
        ydl_opts = {"restrict_filenames": True, "windowsfilenames": False}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            title = meta["title"] + ids
            return self.slugify(title)

    """===============Obtencion de la PlayList==============="""

    def getPlaylist(self, url):
        elem = "abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ids = "".join(random.sample(elem, 4))
        ydl_opts = {
            "username": "baitycasper@gmail.com",
            "password": "$^h5A^TRMtcw6b#q",
            "restrict_filenames": True,
            "windowsfilenames": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            playlist = str(meta["title"]) + ids
            return self.slugify(playlist)

    """===============Descarga de Video de Youtube================="""

    def download(self, url, DIRECTORY, format):
        title = self.getTitle(url)
        file = "./" + DIRECTORY + "/" + title + ".%(ext)s"
        # format = format.split(sep=("("))[-1].replace(")", "")
        opcions = {
            "format": str(format),
            "outtmpl": file,
            "restrict_filenames": True,
            "windowsfilenames": False,
            "progress_hooks": [self.my_hook],
        }

        with yt_dlp.YoutubeDL(opcions) as ydl:
            ydl.download([url])

            # meta = ydl.extract_info(url, download=False)
            name = "./" + DIRECTORY + "/" + title + ".mp4"
            # duration = int(meta['duration'])
        return name

    """================Descarga de Lista de Youtube=================="""

    def downloadlist(self, urls, DIRECTORY):
        playlist = self.getPlaylist(urls)
        file = f"./{DIRECTORY}/{playlist}/%(title)s.%(ext)s"
        # file = './'+playlist+'/%(title)s.%(ext)s'
        ydl_opts = {
            # "format": "bestvideo+bestaudio",
            "format": "b[height<=720]",
            "outtmpl": file,
            "restrict_filenames": False,
            "windowsfilenames": False,
            "progress_hooks": [self.my_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urls])
            dir = f"./{DIRECTORY}/{playlist}"
            name = playlist
            return dir, name
