import yt_dlp

class getInfo():
    def __init__(self, url:str):
        ydl_opts = {
            'simulate': True,
            'gettitle': True,
            'getdescription': True,
            'getduration': True,
            'getuploader': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: info_dict = ydl.extract_info(url, download=False)
        
        self.title = info_dict['title']
        self.description = info_dict['description']
        self.duration = info_dict['duration']
        self.uploader = info_dict['uploader']
        self.formats = info_dict['formats']