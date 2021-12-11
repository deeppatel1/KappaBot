import yfinance as yf


tickers =yf.download(tickers="MSFT", period="5d", interval="1m")



print(tickers)