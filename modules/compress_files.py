from os.path import join, isfile
from os import unlink
from zipfile import ZipFile, ZIP_DEFLATED
from .global_variables import btn_general

def compressFiles(app:object, msg:object, files:list, name_zip:str, dest_folder:str, delete_files=False):
    password = None
    list_string = name_zip.split('\n')
    
    sms_text = msg.reply('**📦 Comprimiendo archivos...**')
    sms_sticker = msg.reply_sticker('./assets/cargando.tgs')

    if len(list_string) >= 2:
        name_zip =  list_string[0]
        password =  list_string[-1]
        
    full_name = join(dest_folder, name_zip + '.zip')
        
    with ZipFile(full_name, 'w') as zip_file:
        if password is None:
            for file in files:
                if isfile(file):
                    zip_file.write(file, compress_type=ZIP_DEFLATED)
                    if delete_files:
                        unlink(file)
        else:
            for file in files:
                if isfile(file):
                    zip_file.write(file, compress_type=ZIP_DEFLATED)
                    if delete_files:
                        unlink(file)
            zip_file.setpassword(password.encode('utf-8'))
    zip_file.close()
    
    app.delete_messages(msg.chat.id, (sms_text.id, sms_sticker.id))
    sms_text.reply_text('**✅ Tarea finalizada**', reply_markup=btn_general)
    return full_name
                
        
    