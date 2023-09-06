import sqlite3
import re


def read_sqlite_table():
    try:
        sqlite_connection = sqlite3.connect('domains.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        res = {}
        sqlite_select_query = """SELECT * from domains"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        print("Вывод каждой строки")
        for row in records:
            project_id = row[0]
            name = row[1]
            j = name.split('.')
            if re.findall('^[a-z]{2,13}$', j[0]):
                if project_id not in res.keys():
                    res[project_id] = r'^\S{2,10}$'
                print(row)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    append_row(res)


def append_row(res):
    try:
        sqlite_connection = sqlite3.connect('domains.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        for k, v in res.items():
            sqlite_insert_with_param = """INSERT INTO rules
                                          (project_id, regexp)
                                          VALUES (?, ?);"""

            data_tuple = (k, v)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


read_sqlite_table()
