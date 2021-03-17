from run_db_operations import execute_select_query
import datetime
import yfinance as yf

# get all data

class TweetOption:
    def __init__(self, ticker, date_time_posted, target_date, target_price, call):
        self.ticker = ticker
        self.date_time_posted = date_time_posted
        self.target_date = target_date
        self.call = call

tweets = execute_select_query("kapp", "SELECT * FROM common_tickers WHERE tweeter='unusual_whales'")

# 
# 
# 
tweets_with_options = []
# 
# 
# 

for each_tweet in tweets:
    if each_tweet[3].startswith("$"):
        info = each_tweet[3].split(" ")
        # current date time:
        now = datetime.datetime.now()
        if info and len(info) >= 4:
            tweet_option = TweetOption(info[0], each_tweet[2], info[1], info[3], info[2] == "C")

            tweets_with_options.append(tweet_option)


worked = 0
failed = 0

for tweet in tweets_with_options:
    now_date_time_obj = datetime.datetime.now()
    if len(tweet.target_date) == 10:
        target_date_time_obj = datetime.datetime.strptime(tweet.target_date, '%Y-%m-%d')

        if now_date_time_obj > target_date_time_obj:
            print('----')
            print(tweet.ticker)
            print(tweet.date_time_posted)
            print(tweet.target_date)
            print(tweet.call)

            ticker_without_dollar = tweet.ticker[1:]

            ticker_info = yf.Ticker(ticker_without_dollar)
            data = ticker_info.history(interval='1d', start=tweet.date_time_posted, end=target_date_time_obj + datetime.timedelta(days=1))
            start_dates_price = data['Open'][0]
            end_dates_price = data['Close'][1]

            change_in_price = end_dates_price - start_dates_price

            print(change_in_price)

            if change_in_price > 0:
                if tweet.call:
                    print("WORKED")
                    worked = worked + 1
                else:
                    failed = failed + 1
            else:
                if not tweet.call:
                    print("WORKED")
                    worked = worked + 1
                else:
                    failed = failed + 1
                

print("*****")
print(worked)
print(failed)
