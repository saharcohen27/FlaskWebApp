import re

class Validator:
    def __init__(self):
        pass

    def check_username(self, username):
        pattern = '^[a-zA-Z0-9]{4,16}$'
        return bool(re.match(pattern, username))

    def check_password(self, password):
        pattern = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,20})'
        return bool(re.match(pattern, password))

    def check_email(self, email):
        pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        return bool(re.match(pattern, email))

    def check_url(self, url):
        pattern = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
        return bool(re.match(pattern, url))