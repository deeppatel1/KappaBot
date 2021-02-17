
# from run_db_operations import execute_select_query, execute_insert_query
import json, psycopg2
"""
WE HAVE INFO FOR::::::

-- loltyler1
-- grossie_gore
-- doublelit
-- xqcow
-- imls
-- itachipower
-- ice
-- deep

"""

with open('./configuration.json') as json_file :
    config = json.load(json_file)

def connect(database):
    try:
        connection = psycopg2.connect(user = config.get("PGUSER"),
                                      password = config.get("PGPASSWORD"),
                                      host = config.get("PGHOST"),
                                      port = config.get("PGPORT"),
                                      database = database)
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        # print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        return cursor, connection

    except Exception as error:
        print("error! " + str(error))


def execute_insert_query(database, query):
    try:
        cursor, connection = connect(database)
        cursor.execute(query)
        connection.commit()
    except Exception as error:
        print("error! " + str(error))


def execute_select_query(database, query):
    try:
        cursor, connection = connect(database)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as error:
        print("error! " + str(error))


"""
Get all info
"""
def get_all_streamer_status_and_info(streamer_name):
    query = "SELECT * FROM streamer_tracker WHERE name = '" + streamer_name + "\'"    
    db_name = "kapp"

    return execute_select_query(db_name, query)

def get_platform_streamers(platform):    
    db_name = "kapp"
    query = "SELECT * FROM streamer_tracker WHERE streamer_platform=\'" + platform + "\'"
    print('--- query')
    print(query)
    return execute_select_query(db_name, query)

def get_everyone_online():
    db_name = "kapp"
    query = "SELECT * FROM streamer_tracker WHERE online=TRUE"
    print('--- query')
    print(query)
    return execute_select_query(db_name, query)


"""
Update specific fields
"""
def update_specific_field(streamer_name, field_to_update, new_value):
    db_name = "kapp"
    query = "UPDATE streamer_tracker SET " + field_to_update + "=\'" + new_value + "\' WHERE name=\'" + streamer_name + "\'"
    return execute_insert_query(db_name, query)


def update_streamer_online_status(streamer_name, new_status):
    status_str = "FALSE"
    
    if new_status:
        status_str = "TRUE"

    update_specific_field(streamer_name, "online", new_status)

def update_viewer_count(streamer_name, new_viewer_count):
    update_specific_field(streamer_name, "viewer_count", new_viewer_count)

def update_video_id(streamer_name, new_video_id):
    update_specific_field(streamer_name, "video_id", new_video_id)

def add_to_tweeter_tickers(tweeter, ticker, date, full_text):
    db_name = "kapp"
    query = "INSERT INTO common_tickers(tweeter, ticker, date, tweet_text) VALUES (\'" + tweeter + "\',\'" + ticker + "\',\'" + date + "\',\'" + full_text + "\')"
    return execute_insert_query(db_name, query)

"""
Get specific fields
"""

def get_streamer_specific_info(streamer_name, column_wanted):

    query = "SELECT " + column_wanted + " FROM streamer_tracker WHERE name = '" + streamer_name + "\'"    
    db_name = "kapp"

    return execute_select_query(db_name, query)    


def get_channel_id(streamer_name):
    return get_streamer_specific_info(streamer_name, "channel_id")


def get_video_id(streamer_name):
    return get_streamer_specific_info(streamer_name, "video_id")


def get_viewer_count(streamer_name):
    return get_streamer_specific_info(streamer_name, "viewer_count")


def get_online_status(streamer_name):
    return get_streamer_specific_info(streamer_name, "online")



# STOCK STUFF

def get_top_stocks(from_date = None, to_date = None):

    print("input from an to date")
    print(from_date)
    print(to_date)
    # If no dates are provided, get top 10 tickers all time:

    if not from_date and not to_date:   
        query = "SELECT f.ticker, array_agg(f.tweeter) as all_tweeters, array_length(array_agg(f.tweeter), 1) FROM (SELECT DISTINCT d.tweeter, lower(d.ticker) as ticker FROM (SELECT * from common_tickers WHERE date >= '2021-02-14') as d) as f GROUP BY ticker ORDER BY array_length DESC limit 8"

    if from_date and not to_date:
        query = "SELECT f.ticker, array_agg(f.tweeter) as all_tweeters, array_length(array_agg(f.tweeter), 1) FROM (SELECT DISTINCT d.tweeter, lower(d.ticker) as ticker FROM (SELECT * from common_tickers WHERE date >= \'" + from_date + "\') as d) as f GROUP BY ticker ORDER BY array_length DESC limit 8"

    if from_date and to_date:
        query = "SELECT f.ticker, array_agg(f.tweeter) as all_tweeters, array_length(array_agg(f.tweeter), 1) FROM (SELECT DISTINCT d.tweeter, lower(d.ticker) as ticker FROM (SELECT * from common_tickers WHERE date >= \'" + from_date + "\' AND date <= \'" + to_date + "\') as  d) as f GROUP BY ticker ORDER BY array_length DESC limit 8"
        # query = "SELECT f.ticker,array_agg(f.tweeter) as tweeters,  COUNT(f.ticker) as ticker_mention_count FROM (SELECT DISTINCT tweeter, date, lower(ticker) AS ticker, date FROM common_tickers WHERE date >= \'" + from_date + "\' AND date <= \'" + to_date + "\') as f GROUP BY ticker, tweeter ORDER BY ticker_mention_count DESC LIMIT 6"
    print(query)
    resp = execute_select_query("kapp", query)

    # final_str = ""

    # for a in resp:
    #     ticker = a[0]
    #     ticker_count = a[1]
    #     final_str = final_str + '{:<10}{:>4}\n'.format(ticker.rstrip(), str(ticker_count))

    return resp


def get_specific_tickers(ticker):
    # SELECT tweeter, lower(ticker) AS ticker, date, tweet_text from common_tickers where ticker = '$tsla'

    query = "SELECT tweeter, ticker, date, tweet_text from common_tickers where LOWER(ticker) = \'$" + ticker.lower() + "\' ORDER BY date DESC limit 25"
    print(query)
    resp = execute_select_query("kapp", query)
    return resp