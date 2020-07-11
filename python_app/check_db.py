import psycopg2, json


with open('configuration.json') as json_file :
    config = json.load(json_file)

def connect():
    try:
        connection = psycopg2.connect(user = config.get("PGUSER"),
                                      password = config.get("PGPASSWORD"),
                                      host = config.get("PGHOST"),
                                      port = config.get("PGPORT"),
                                      database = config.get("PGDATABASE"))
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        return cursor, connection

    except Exception as error:
        print("error! " + error)


def execute_insert_query(query):
    try:
        cursor, connection = connect()
        cursor.execute(query)
        connection.commit()
    except Exception as error:
        print("error! " + error)


def execute_select_query(query):
    try:
        cursor, connection = connect()
        cursor.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as error:
        print("error! " + error)