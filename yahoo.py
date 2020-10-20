import yfinance as yf
import time

start_time = time.time()
msft = yf.Ticker("MSFT")
print(msft.info)
print("YAHOO --- %s seconds ---" % (time.time() - start_time))