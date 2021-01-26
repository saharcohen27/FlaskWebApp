from classes.DataBase import Database
from flask import request, session
import uuid

class User:
    def __init__(self):
        try:
            self._id = request.cookies.get('CookieID') or session['SessionID']
        except KeyError:
            pass

    def username(self):
        result = Database().ask(f"SELECT Username FROM SessionsAndCookies WHERE SessionID = '{self._id}' OR CookieID = '{self._id}';")
        if result:
            return result[0][0]
        return "Anonymous"

    def get_email(self, _id):
        result = Database().ask(f"SELECT EmailAddress FROM SessionsAndCookies WHERE SessionID = '{_id}' OR CookieID = '{_id}';")
        if result:
            return result[0][0]
            
    def is_logged(self):
        is_cookie_logged = is_session_logged = False
        if 'CookieID' in request.cookies:
            is_cookie_logged = self.__logged(request.cookies['CookieID'])
        if 'SessionID' in session:
            is_session_logged = self.__logged(session['SessionID'])
        return is_session_logged or is_cookie_logged

    def __logged(self, _id):
        return True if Database().ask(f"SELECT * FROM SessionsAndCookies WHERE SessionID = '{_id}' OR CookieID = '{_id}';") else False

    def logout(self, _id): 
        Database().ask(f"DELETE FROM SessionsAndCookies WHERE SessionID = '{_id}' OR CookieID = '{_id}';")

    def login_SAC(self, username, cookie=False):

        session_id = uuid.uuid4()
        Database().ask(f"INSERT INTO SessionsAndCookies (Username, SessionID) VALUES ('{username}', '{session_id}');")
        
        if cookie:
            # user wants cookie too (rememeber him next time he log in)
            cookie_id = uuid.uuid4()
            Database().ask(f"UPDATE SessionsAndCookies SET CookieID='{cookie_id}' WHERE Username='{username}';")
            return (str(session_id), str(cookie_id))
        
        return str(session_id)
