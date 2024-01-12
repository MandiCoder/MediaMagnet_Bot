from os.path import join, isfile
from zipfile import ZipFile, ZIP_DEFLATED
from .global_variables import btn_general

def compressFiles(app:object, msg:object, files:list, name_zip:str, dest_folder:str):
    password = None
    list_string = name_zip.split('\n')
    
    sms_text = msg.reply('**📦 Comprimiendo archivos...**')
    sms_sticker = msg.reply_sticker('./assets/cargando.tgs')

    if len(list_string) >= 2:
        name_zip =  list_string[0]
        password =  list_string[-1]
        
    with ZipFile(join(dest_folder, name_zip + '.zip'), 'w') as zip_file:
        if password is None:
            for file in files:
                zip_file.write(file, compress_type=ZIP_DEFLATED)
        else:
            for file in files:
                zip_file.write(file, compress_type=ZIP_DEFLATED)
            zip_file.setpassword(password.encode('utf-8'))
    zip_file.close()
    
    app.delete_messages(msg.chat.id, (sms_text.id, sms_sticker.id))
    return sms_text.reply_text('**✅ Tarea finalizada**', reply_markup=btn_general)
                
        
    