
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

