
from flask import Blueprint, request, render_template, url_for, session, redirect, abort, jsonify
import json
from classes.DataBase import Database
from classes.user import User

profiles = Blueprint('profiles', __name__)

@profiles.route('/profile', methods=['POST', 'GET'])
def profile():
    username = User().username()
    if request.method == 'POST':
        try:
            new_desc = request.json['desc']
            Database().update_desc(username, new_desc)
            return jsonify(success=True, payload={ "desc": request.json["desc"] }, message="Description updated.")
        except:
            return jsonify(success=False, error={ "code": 400, "message": "description is required. ('desc')" })
    else:
        user_data = Database().get_user(username)
        return render_template('profile.html', userData = user_data)
    

@profiles.route('/users/<user>')
def user(user):
    if user == User().username():
        return redirect('/profile')

    if Database().is_user(user):
        user_data = Database().get_user(user)
        return render_template('user.html', userData=user_data)
    else:
        abort(404)

