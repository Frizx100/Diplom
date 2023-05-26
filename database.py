import sqlite3

database = 'Diplom.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def run_query(text, is_fetchone):
    try:
        sqlite_connection = sqlite3.connect(database)
        sqlite_connection.row_factory = dict_factory
        cursor = sqlite_connection.cursor()
        cursor.execute(text)

        if is_fetchone is True:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        print(result)    
        return result

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

def post_data(text):
    try:
        sqlite_connection = sqlite3.connect(database)
        cursor = sqlite_connection.cursor()
        cursor.execute(text)
        sqlite_connection.commit()
        # print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()
        return 'OK'
        
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return None

def delete_data(text):
    try:
        sqlite_connection = sqlite3.connect(database)
        cursor = sqlite_connection.cursor()
        cursor.execute(text)
        sqlite_connection.commit()
        # print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()
        return 'OK'
        
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return None    