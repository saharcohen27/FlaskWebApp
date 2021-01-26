from flask import Flask, render_template, session, request, url_for, redirect, send_from_directory
from classes.user import User
import os

from routes.other import other
from routes.auth import auth
from routes.profiles import profiles
from routes.lives import lives
from routes.crypto import crypto

app = Flask(__name__)
app.secret_key = 'S3cR37-K3y'
app.register_blueprint(other, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(profiles, url_prefix='/')
app.register_blueprint(lives, url_prefix='/')
app.register_blueprint(crypto, url_prefix='/')

@app.errorhandler(404)
def error404(error):
    return render_template('error404.html')

@app.after_request
def add_header(r):
    """
    Disable caching
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

no_login_required = ['login', 'register']

@app.before_request
def check_if_user_connected():
    if not User().is_logged():
        # if user is not connected
        url = request.url.split('/')
        route = url[3]
        if route not in no_login_required and len(url) == 4:
            return redirect('/login')
    

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, port=2222)


# TODOS:
    # fix
        # [X] top rigth navbar Logout button

    # small
        # [X] add alert message when login uncsuccessful ~ 2h
        # [X] add alert message when regsiter uncsuccessful ~ 2h

    # medium
        # [] find api and generate coins list for crypro page ~ 4h
    
    # big
        # [] followers system
        # [] portfolio system