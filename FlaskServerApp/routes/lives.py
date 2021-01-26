from flask import Blueprint, url_for, render_template, session, request, jsonify, abort, redirect, send_from_directory
from classes.DataBase import Database
from classes.user import User
import time

lives = Blueprint('lives', __name__)

@lives.route('/live/<username>')
def live_page(username):
    # TODO change to is user and check if is he streaming right now!
    if not Database().is_user(username):
        abort(404)
    return render_template('livestream.html', streamer=username)

@lives.route('/live')
def live():
    username = User().username()
    if Database().is_streamer_username(username):
        return render_template('livestreamControl.html', key=Database().get_streamer_key(username))
    return render_template('createStreamAccount.html')
    

@lives.route('/video/<string:file_name>')
def stream(file_name):
    video_dir = './video'
    return send_from_directory(directory=video_dir, filename=file_name)