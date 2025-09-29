from pg.pg_con import dbConnection

db = dbConnection()


def add_tables_users():
    '""Добавление таблицы users"""'
    "Добавление таблицы users"
    query = """CREATE TABLE users (
    chat_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    phone VARCHAR(255),
    verification_code integer, 
    registered boolean,
    verification boolean
    )"""
    return query


def add_tables_task():
    '""Добавление таблицы Task"""'
    "Добавление таблицы Task"
    query = """CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR,
    customer_task integer,
    contractor_task integer
    )"""
    return query


def save_data_in_tasks(tablename, chat_id):
    """Сохранение данных в таблицу tasks"""
    query = f"""INSERT INTO {tablename} (chat_id) VALUES (%s) ON CONFLICT (chat_id) DO NOTHING"""
    value = (chat_id,)
    db.execute(query, value)
    return True


def get_course(date):
    '""Получение курса валюты по дате"""'
    query = f"""
    SELECT course FROM currency_course WHERE date = '{date}' LIMIT 1
    """
    res = db.fetchone(query)
    if res is not None:
        value = res[0]
        float_value = float(value)
        # print(float_value)
        return float_value
    else:
        return None


def save_data_in_course(date, course):
    """Сохранение курса валюты"""
    query = """INSERT INTO currency_course (date, course) VALUES (%s, %s) ON CONFLICT (date) DO NOTHING"""
    value = (
        date,
        course,
    )
    db.execute(query, value)
    return True


def update_flag_in_table_flags(chat_id, value):
    """Обновление флага в таблице flags"""
    base_query = f"UPDATE flags SET flags = %s WHERE chat_id = {chat_id}"
    value = (value,)
    db.execute(base_query, value)
    return True


def check_user_in_flags(chat_id):
    """Проверка на наличие флага в таблице flags"""
    res = db.checking_for_db("flags", "chat_id", chat_id)

    if res:
        flag = db.get_date_pg("flags", "flags", "chat_id", chat_id)[0]

        return flag
    else:
        base_query = f"INSERT INTO flags (chat_id) VALUES ({chat_id}) ON CONFLICT (chat_id) DO NOTHING"
        # value = (chat_id)
        # query = base_query.format(value)
        db.execute(base_query)
        return None


def save_data_in_table_users_one(columns, value, chat_id):
    """Сохранение данных в таблицу users"""
    base_query = f"UPDATE users SET {columns} = %s WHERE chat_id = {chat_id}"
    value = (value,)
    db.execute(base_query, value)
    return True


def get_last_id_order():
    """Получение последнего id заказа"""
    base_query = "SELECT id_order FROM orders ORDER BY id_order DESC LIMIT 1;"
    last_id = db.fetchone(base_query)
    return last_id


def save_data_pre_order(chat_id, city):
    """Сохранение данных в таблицу pre_order"""
    base_query = """INSERT INTO pre_order (chat_id, delivery_direction)
VALUES (%s, %s)
ON CONFLICT (chat_id)
DO UPDATE SET
    delivery_direction = EXCLUDED.delivery_direction,
    insurance = NULL,
    link_product = NULL,
    img_color = NULL,
    img_size = NULL,
    count = NULL,
    price = NULL,
    amount = NULL;"""

    db.execute(base_query, (chat_id, city))
    return True


def save_data_in_table_pre_order_one(columns, value, chat_id):
    """Сохранение данных в таблицу pre_order"""
    base_query = f"UPDATE pre_order SET {columns} = %s WHERE chat_id = {chat_id}"
    value = (value,)
    db.execute(base_query, value)
    return True


async def get_data_in_table(tablename, where_columns, value_columns):
    """Получаю Словарь"""
    # Получаю данные из таблицы по условию
    query = f"""SELECT * FROM {tablename} WHERE {where_columns} = %s"""
    value = (value_columns,)
    res = db.execute_dict_one_record(query, value)
    # res = res.get("exists")
    return res


async def get_data_in_table_all(tablename, where_columns, value_columns):
    """Получаю Словарь"""
    # Получаю данные из таблицы по условию
    query = f"""SELECT * FROM {tablename} WHERE {where_columns} = %s"""
    value = (value_columns,)
    res = db.execute_list_all_record(query, value)
    # res = res.get("exists")
    return res


async def save_data_in_table_orders(data, id_order, chat_id):
    '""Сохранение данных в таблицу orders"""'
    """Получаю Словарь"""
    amount = int(data.get("count")) * float(data.get("price"))
    query = """INSERT INTO orders (
            id_order, chat_id, delivery_direction, insurance,
            link_product, img_product, img_color, img_size,
            count, price, amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    params = (
        id_order,
        chat_id,
        data.get("delivery_direction"),
        data.get("insurance"),
        data.get("link_product"),
        data.get("img_product"),
        data.get("img_color"),
        data.get("img_size"),
        int(data.get("count")),
        float(data.get("price")),
        amount,
    )
    # value = (value_columns,)
    res = db.execute(query, params)
    # res = res.get("exists")
    return res


async def clear_pre_order(chat_id):
    """Очистка таблицы pre_order"""
    query = f"""UPDATE pre_order
        SET
            delivery_direction = NULL,
            insurance = NULL,
            link_product = NULL,
            count = NULL,
            price = NULL,
            amount = NULL,
            img_product = NULL,
            img_color = NULL,
            img_size = NULL,
            id_order = NULL
        WHERE chat_id = {chat_id};"""
    res = db.execute(query)
    return res
