import time
import requests

tickers = ['ENPG.ME','AFKS.ME','AFLT.ME','VTBR.ME','IRAO.ME','MTSS.ME','SBER.ME','FLOT.ME','ENRU.ME','AAPL']


def get_json(tickers):
    url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols='+','.join(tickers)
    data = requests.get(url).json()['quoteResponse']['result']
    return data if len(data) > 1 else data[0]
        

def main():
    start_time = time.time()
    data_json = get_json(tickers)
    for ticker in data_json:
        print(f'{ticker["symbol"]}: {ticker["regularMarketPrice"]} {ticker["currency"]}')
    print("YAHOO --- %s seconds ---" % (time.time() - start_time))


def find_ticker(ticker, stock):
    """Finds ticker on Yahoo.Finance return True if exists"""
    stock_url = '' if stock == 'NSDQ' else f'.{stock}'
    url = f'https://query1.finance.yahoo.com/v1/finance/search?q={ticker}{stock_url}&lang=en-US&quotesCount=10&newsCount=0'
    data = requests.get(url).json()
    if data['count'] == 0: return False
    for q in data['quotes']:
        if q['symbol'] == f'{ticker}{stock_url}': return True
    return False
    

if __name__ == '__main__':
    print(find_ticker('aapl'.upper(), 'nsdq'.upper()))
