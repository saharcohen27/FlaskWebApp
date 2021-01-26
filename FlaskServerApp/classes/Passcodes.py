import smtplib, string, random
from classes.DataBase import Database

class Passcodes:
    EMAIL_ADDRESS = "cyberprojectsahar@gmail.com"
    PASSWORD = "NO..."
    PASSCODE_LENGTH = 8

    def __init__(self):
        self.server = None
    
    def close_conn(self):
        try:
            self.server.quit()
        except smtplib.SMTPServerDisconnected:  # server probably already crashed
            pass

    def login(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(Passcodes.EMAIL_ADDRESS, Passcodes.PASSWORD)

    def generate_passcode(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def send_mail(self, username, passcode):
        receiver = Database().get_user(username)[1] # = email 
        message = f"Hello {username}! \n Here is your passcode: {passcode}"
        message = 'Subject: {}\n\n{}'.format("You Got The Passcode!", message)
        self.server.sendmail(Passcodes.EMAIL_ADDRESS, receiver, message.encode())

    def send_email(self, username):
        
        if Database().ask(f"SELECT * FROM Passcodes WHERE Username='{username}';") or \
           Database().ask(f"SELECT * FROM Streamers WHERE Username='{username}';"):
            return False
        
        self.login()
        
        passcode = self.generate_passcode(Passcodes.PASSCODE_LENGTH)
        while Database().ask(f"SELECT * FROM Passcodes WHERE Passcode='{passcode}';"):
            passcode = self.generate_passcode(Passcodes.PASSCODE_LENGTH)

        Database().ask(f"INSERT INTO Passcodes (Username, Passcode) VALUES ('{username}', '{passcode}');")
        
        self.send_mail(username, passcode)
        
        self.close_conn()

        return True


    def verify_passcode(self, username, given_passcode):
        correct_passcode = Database().ask(f"SELECT Passcode FROM Passcodes WHERE Username='{username}';")[0][0]
        
        if not correct_passcode:
            return False # in case the user does not even waiting for verification
        
        if correct_passcode == given_passcode:
            Database().ask(f"DELETE FROM Passcodes WHERE Passcode='{correct_passcode}';")
            return True
            
        return False
