from mediafire.client import MediaFireClient
from os import listdir
from os.path import join

client = MediaFireClient()
client.login(email="baitycasper@gmail.com", password="Spar1Syco7Shri0%", app_id="42511")

path = "downloads/MandiCoder"
for i in listdir(path):
    full_path = join(path, i)
    var = client.upload_file(full_path, "mf:/Videos/")
    print(f"https://www.mediafire.com/file/{var.quickkey}/{var.filename}/file")
