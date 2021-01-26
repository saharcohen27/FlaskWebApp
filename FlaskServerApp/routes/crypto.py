from flask import Blueprint, request, render_template, url_for, session, redirect, abort
import time
import threading
import ast
import requests
from classes.api_cmc import CoinMarketCap

crypto = Blueprint('crypto', __name__)
    

@crypto.route('/crypto')
def crypto_market():
    global coins
    return render_template('crypto.html', currencies=coins)


@crypto.route('/crypto/<name>')
def cryptocurrency(name):
    global charts
    global coins

    for coin in coins: 
        if coin[1] == name:
            return render_template('coin.html', coin=coin, history=charts[name.lower()])
    
    abort(404)
    
def data():
    global charts
    global coins
    coins = CoinMarketCap().request()
    session = requests.Session()
    charts = {}
    # while True:
    try:
        for coin in coins:
            coingeko_api = f"https://api.coingecko.com/api/v3/coins/{coin[1].lower()}/ohlc?vs_currency=usd&days=365"
            response = session.get(coingeko_api)
            this = ast.literal_eval(response.content.decode())
            charts[coin[1].lower()] = this
        # time.sleep(60000)
    except:
        print("ERROR")

t = threading.Thread(target=data)
t.start()
