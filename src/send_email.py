from email.message import EmailMessage
import smtplib
from tkinter import messagebox as msg
def email_alert(subject, body, to):
    try:
        message = EmailMessage()
        message.set_content(body)
        message['subject'] =  subject
        message['to'] = to
        user  = 'danielmaishy@gmail.com'
        message['from'] = user
        password = 'sjrzqhhrytnfgkow'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(message)
        server.quit()
    except Exception as e:
        msg.showerror('error',f"Error: {e}")


    



    