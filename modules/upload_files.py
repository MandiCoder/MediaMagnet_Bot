
def uploadFile(app, msg, file):
    sms = msg.reply(f'**Subiendo: `{file.split("/")[-1]}`...**')
    
    app.send_document(msg.chat.id, file)
    sms.delete()