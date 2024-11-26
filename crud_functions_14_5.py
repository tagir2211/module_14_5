import sqlite3

from text import *

connection = sqlite3.connect("Telegram.db")
cursor = connection.cursor()


def initiate_db(table, param):
    sql_text = ''
    sql_text += f"CREATE TABLE IF NOT EXISTS {table}("
    for key, value in param.items():
        if key == list(param.keys())[0]:
            sql_text += f"{key.lower()} {value.upper()} PRIMARY KEY"
        else:
            if value[1]:
                sql_text += f", {key.lower()} {value[0].upper()} NOT NULL"
            else:
                sql_text += f", {key.lower()} {value[0].upper()}"
    sql_text += ")"
    cursor.execute(sql_text)
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_email ON {table} ({list(param.keys())[0].lower()})")
    connection.commit()


def add_in_db(table, param):
    sql_text = ''
    sql_text += f'INSERT INTO {table}('
    for key in param.keys():
        if key == list(param.keys())[-1]:
            sql_text += f'{key}) VALUES ('
        else:
            sql_text += f"{key}, "
    for value in param.values():
        if value == list(param.values())[-1]:
            sql_text += f'"{value}")'
        else:
            sql_text += f'"{value}", '
    cursor.execute(sql_text)
    connection.commit()


def get_all_products(name, id):
    cursor.execute(f"SELECT * FROM {name} WHERE id = ?", (id,))
    product = cursor.fetchall()
    return f'Название: {product[0][1]} | Описание: {product[0][2]} | Цена: {product[0][3]}'


def is_included(table, search):
    '''

    :param table: название таблицы в которой проверяем наличе, строка
    :param search: параетры по кторому идет поиск, словарь где key это имя поля (строка), value значеие в поле key  (строка)
    :return: True|False
    '''
    cursor.execute(f'SELECT * FROM {table} WHERE "{list(search.keys())[0]}" = "{list(search.values())[0]}"')
    result = cursor.fetchall()
    return result != []


# initiate_db("Products",
#             {'id': 'integer', 'title': ['text', True], 'description': ['text', False], 'price': ['integer', True]})
#
# for i in range(4):
#     add_in_db("Products", {'title': title[i], 'description': info[i], 'price': price[i]})
#
# initiate_db("users", {'id': 'integer', 'username': ['text', True], 'email': ['text', True], 'age': ['integer', True],
#                       'balance': ['integer', True]})
#
# for i in range(4):
#     print(i)
#     print(get_all_products("Products", i + 1))
# print('ok')
#
#
# print(is_included('Products', {'title':  title[1]}))
#
# connection.commit()
# connection.close()
