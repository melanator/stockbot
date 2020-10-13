import requests


def get_json(ticker):
    url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/' \
          'tqbr/securities.jsonp?iss.meta=off&iss.only=marketdata&securities='+ticker
    r = requests.get(url).json()
    return dict(zip(r['marketdata']['columns'], r['marketdata']['data'][0]))


def get_last_price(json):
    return json['LAST']


if __name__ == '__main__':
    info = get_json('ENPG')
    print(get_last_price(info))
