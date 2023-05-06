import psycopg2, json


with open('./configuration.json') as json_file :
    config = json.load(json_file)


CURSOR = None
CONNECTION = None


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
        if not CURSOR or not CONNECTION:
            CURSOR, CONNECTION = connect(database)
        
        CURSOR.execute(query)
        CONNECTION.commit()
    except Exception as error:
        print("error! " + str(error))


def execute_select_query(database, query):
    try:
        if not CURSOR or not CONNECTION:
            CURSOR, CONNECTION = connect(database)
        
        CURSOR.execute(query)
        rows = CURSOR.fetchall()
        return rows

    except Exception as error:
        print("error! " + str(error))
