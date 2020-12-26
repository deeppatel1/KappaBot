import psycopg2, json


with open('../configuration.json') as json_file :
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
        print ( connection.get_dsn_parameters(),"\n")
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


execute_select_query("cx_network", "SELECT * FROM ")