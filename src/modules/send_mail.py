import smtplib
from email.message import EmailMessage
import ssl

def sendMail(message:str):
    receiver = 'baitycasper@gmail.com'

    smtp_server = 'smtp.gmail.com'
    smtp_port = 1025
    smtp_username='reynaldo.magdariaga@gmail.com'
    smtp_password = 'eotd kqsb whvc qbqz'
        
    msg=EmailMessage()
    msg['From']=smtp_username
    msg['To'] = receiver
    msg['Subject']='Aviso'
    msg.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls(context=context)
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(smtp_username, receiver, msg.as_string())

