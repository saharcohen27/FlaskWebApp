from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class CoinMarketCap():
    def __init__(self):
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'No...',
        }
    
    def send_request(self, url, parameters=None):
        session = Session()
        session.headers.update(self.headers)
        response = session.get(url, params=parameters)
        self.data = json.loads(response.text)

    def request(self):
        parameters = {
            'start':'1',
            'limit':'100',
            'convert':'USD'
        }
        
        try:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            self.send_request(url, parameters)
            self.create_table()

            url2 = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id=" + ','.join(self.ids)
            self.send_request(url2)
            self.add_logos()
            return self.currencies_list
            
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            pass

    def add_logos(self):
        index = 0
        for currency in self.currencies_list:
            currency.append(self.data['data'][self.ids[index]]['logo'])
            index += 1

    def create_table(self):
        self.currencies_list = []
        self.ids = []
        index = 1

        for currency in self.data['data']:
            temp = [
                    str(index), 
                    currency['name'], 
                    f"{currency['quote']['USD']['price']:,}" + '$',
                    f"{currency['quote']['USD']['market_cap']:,}" + '$',
                    currency['quote']['USD']['percent_change_24h'],
                    f"{currency['quote']['USD']['volume_24h']:,}" + '$',
                    f"{currency['circulating_supply']:,}" + ' ' + str(currency['symbol']),
                ]

            self.currencies_list.append(temp)
            self.ids.append(str(currency['id']))
            index += 1
