from flask import Blueprint, redirect, render_template, session, request, url_for, jsonify, abort
from classes.Passcodes import Passcodes
from classes.user import User
from classes.DataBase import Database

other = Blueprint('other', __name__)

@other.route('/')
def main_page():
    return render_template('mainpage.html', username=User().username())


@other.route('/passcodes', methods=['POST', 'GET'])
def passcodes():
    if request.method == 'GET':
        abort(404)

    elif request.method == 'POST':
        try:
            username = User().username()
            if request.json['request'] == 'sendEmail':
                success = Passcodes().send_email(username)
                if success:
                    return jsonify(success=True, message="Email Has Been Sent.")
                return jsonify(success=False, error={ "code": 400, "message": "We already sent you the email." })

            
            elif request.json['request'] == 'verifyPasscode':
                if not (Database().is_user(username) and Passcodes().verify_passcode(username, request.json['passcode'])):
                    return jsonify(success=False, error={ "code": 401, "message": "Worng passcode." })
                
                success = Database().create_stream_account(username)
                if success:
                    return jsonify(success=True, message="Passcode verified and stream account has been created.")
                
                return jsonify(success=False, error={ "code": 401, "message": "Stream account is already exists." })

            else:
                return jsonify(success=False, error={ "code": 400, "message": "You can either send 'sendEmail' or 'verifyPasscode' requests in 'request'." })
        
        except:
            return jsonify(success=False, error={ "code": 400, "message": "'request' is required." })

