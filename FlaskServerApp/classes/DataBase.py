import sqlite3, datetime
try:
    from classes.Validation import Validator
except:
    # TODO remove later! dev mode!
    from Validation import Validator
import hashlib
import uuid 

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.database_file = "database.db"

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_file)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("[CONNECTION ERROR!] ", e)

    def close(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print("[CLOSE CONNECTION ERROR!] ", e)

    def ask_only(self, sql):
        try:
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print("[SQL ASK ERROR!] ", e)
    
    def ask(self, sql):
        self.connect()
        data = self.ask_only(sql)
        self.close()
        return data

    def add_user(self, name, email, password):
        if Validator().check_username(name) and \
            Validator().check_email(email) and \
            Validator().check_password(password): 

            data = self.ask(f"SELECT * FROM Users WHERE Username='{name}' OR EmailAddress='{email}'")
            if not data:
                encrypted_password = hashlib.md5(password.encode()).hexdigest()
                self.ask(f"INSERT INTO Users (Username, EmailAddress, Pwd, CreatedAt) VALUES ('{name}','{email}','{str(encrypted_password)}','{str(datetime.datetime.now())}');")
                return True

        return False
    
    def is_google_user(self, username):
        data = self.ask(f"SELECT googleUser From Users WHERE Username='{username}';")[0][0]
        return data == 'True'

    def add_google_user(self, username, email, image_url):
        if Validator().check_username(username) and Validator().check_email(email) and Validator().check_url(image_url):
            data = self.ask(f"SELECT * FROM Users WHERE Username='{username}'")
            if not data:
                self.ask(f"INSERT INTO Users (Username, EmailAddress, CreatedAt, ImageUrl, googleUser) VALUES ('{username}','{email}','{datetime.datetime.now()}','{image_url}', 'True');")
            return True
        return False
        
    def delete_user(self, username):
        self.ask(f"DELETE FROM Users WHERE Username='{username}'")

    def get_all_data(self):
        return self.ask(f"SELECT * FROM Users")
    
    def login(self, username, password):
        encrypted_password = hashlib.md5(password.encode()).hexdigest()
        data = self.ask(f"SELECT * FROM Users WHERE Username='{username}' AND Pwd='{str(encrypted_password)}'")
        return True if data else False
    
    def get_user(self, username):
        try:
            return self.ask(f"SELECT * FROM Users WHERE Username='{username}'")[0]
        except IndexError:
            return ""

    def update_desc(self, username, new_desc):
        self.ask(f"UPDATE Users SET Description='{new_desc}' WHERE Username='{username}';")

    def is_user(self, username):
        return True if self.get_user(username) else False

    def is_google_user_by_email(self, email):
        data = self.ask(f"SELECT googleUser From Users WHERE EmailAddress='{email}';")
        return True if data else False

    def get_user_by_email(self, email):
        try:
            return self.ask(f"SELECT Username From Users WHERE EmailAddress='{email}' AND googleUser IS NULL;")[0][0]
        except IndexError:
            return False

    def email_exist(self, email):
        data = self.ask(f"SELECT Username From Users WHERE EmailAddress='{email}';")
        return True if data else False

    def make_google(self, username_to_update, img):
        self.ask(f"UPDATE Users SET ImageUrl='{img}', googleUser='True' WHERE Username='{username_to_update}';")

    def get_googleuser_by_email(self, email):
        try:
            return self.ask(f"SELECT Username From Users WHERE EmailAddress='{email}' AND googleUser IS NOT NULL;")[0][0]
        except IndexError:
            return False

    def is_streamer_username(self, username):
        try:
            self.ask(f"SELECT * FROM Streamers WHERE Username='{username}'")[0]
            return True
        except IndexError:
            return False
    
    def __create_account(self, username):
        self.ask(f"INSERT INTO Streamers (Username, StreamKey, IsLive) VALUES('{username}', '{uuid.uuid4()}', 'False');")

    def create_stream_account(self, username):
        if self.is_streamer_username(username):
            return False
        self.__create_account(username)
        return True
    
    def get_streamer_key(self, username):
        return self.ask(f"SELECT StreamKey FROM Streamers WHERE Username='{username}';")[0][0]
