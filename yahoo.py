import time
import requests


tickers = ['ENPG.ME','AFKS.ME','AFLT.ME','VTBR.ME','IRAO.ME','MTSS.ME','SBER.ME','FLOT.ME','ENRU.ME','AAPL']

def get_json(tickers):
    url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols='+','.join(tickers)
    #return_dict = {}
    #r = requests.get(url).json()['quoteResponse']['result']
    #for ticker in r:
    #    return_dict[ticker['symbol']] = ticker
    return requests.get(url).json()['quoteResponse']['result']
        

def main():
    start_time = time.time()
    data_json = get_json(tickers)
    for ticker in data_json:
        print(f'{ticker["symbol"]}: {ticker["regularMarketPrice"]} {ticker["currency"]}')
    print("YAHOO --- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
