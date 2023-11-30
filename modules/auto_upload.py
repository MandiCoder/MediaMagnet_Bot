from os import listdir, makedirs, unlink, rmdir
from os.path import join
from modules.upload_files import uploadFile
from .download_files import downloadFiles
from time import sleep


def autoUpload(app, msg, path_download, userbot, url):
    makedirs(path_download)
    sms = downloadFiles(app, msg, path_download, userbot, url)
    sms.delete()
    
    for i in listdir(path_download):
        file = join(path_download, i)
        uploadFile(app, msg, file, msg.from_user.username)
        unlink(file)
        sleep(5)
    
    rmdir(path_download)