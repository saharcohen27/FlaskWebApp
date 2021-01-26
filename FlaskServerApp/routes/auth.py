from flask import Blueprint, request, render_template, url_for, make_response, session, redirect, jsonify, abort
import json
from classes.DataBase import Database
from classes.user import User

auth = Blueprint('auth', __name__)

def regular_login():
    username = request.form['uname']
    password = request.form['psw']
    to_remember = request.form.get('remember')
    
    if not Database().login(username, password):
        return render_template('login.html', unsuccessfully=True)

    response = make_response(redirect('/'))
    
    if str(to_remember) == 'on':
        session_id, cookie_id = User().login_SAC(username, True)
        response.set_cookie('CookieID', cookie_id, max_age=60*60*24*365*2)
    else:
        session_id = User().login_SAC(username)

    session['SessionID'] = session_id

    return response


def google_login1(google_data):
    valid = success = True
    if Database().email_exist(google_data['email']):
        username = Database().get_user_by_email(google_data['email'])
        if username:
            # google login after regular sign up (same email) -> updating data
            Database().make_google(username, google_data['image'])
        else:
            # google login after google login -> regular successful google login
            username = Database().get_googleuser_by_email(google_data['email'])
            
    else:
        username = google_data['email'].split('@')[0] # default username
        if Database().is_user(username):
            # first google login and username is taken -> asking to chose another username (after that, google_login2 should run)
            success = False
        else:
            # first google logn and username is not taken -> creating new account
            valid = Database().add_google_user(username, google_data['email'], google_data['image'])
    
    return (valid, success, username)


def google_login2(google_data):
    valid = True
    username = google_data['username']
    success = not Database().is_user(username)
    if success:
        valid = Database().add_google_user(username, google_data['email'], google_data['image']) 
    return (valid, success, username)
    

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            if not request.json:
                return regular_login()

            google_data = request.json

            if google_data['try'] == 1:
                valid, success, username = google_login1(google_data)
            
            elif google_data['try'] == 2:
                valid, success, username = google_login2(google_data)
                    
            else:
                return jsonify(success=False, error={ "code": 400, "message": "The try number should be 1 or 2." })


            if not valid:
                return jsonify(success=False, error={ "code": 400, "message": "Invalid Email/Image/Username data format." })


            if success:
                response = make_response(jsonify(success=True, message="Google User Logged In."))
                session_id, cookie_id = User().login_SAC(username, True)
                session['SessionID'] = session_id
                response.set_cookie('CookieID', cookie_id, max_age=60*60*24*365*2) # saved for 2 years
                return response

            return jsonify(success=False, error={ "code": 400, "message": "Username is already taken." })
            
        except Exception:
            return jsonify(success=False, error={ "code": 400, "message": "'try'/'email'/'image' (and 'username' for try number 2) Are Required." })


    else:
        if User().is_logged():
            return redirect('/')
        else:
            return render_template('login.html', unsuccessfully=False)


@auth.route('/logout')
def logout():
    res = make_response(redirect('/login'))
    if 'CookieID' in request.cookies: User().logout(request.cookies['CookieID'])
    if 'SessionID' in session: User().logout(session['SessionID'])
    res.set_cookie('CookieID', '', expires=0)
    session.pop('SessionID', None)
    return res


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            email = request.json.get('email')
            password = request.json.get('psw')
            username = request.json.get('uname')
            success = Database().add_user(username, email, password)
            if success:
                return jsonify(success=True, message="The account has been created.")
            return jsonify(success=False, error={ "code": 400, "message": "Register Failed. email/password/username are not valid." })
        except:
            return jsonify(success=False, error={ "code": 400, "message": "'email'/'psw'/'uname' Are Required. (some missing)" })

    return redirect('/') if User().is_logged() else render_template('register.html')
