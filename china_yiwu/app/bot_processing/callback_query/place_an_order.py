import os

import telegram

from bot_processing.func import (
    get_phone,
    keyboard_add_product,
    keyboard_delivery_direction,
    keyboard_insurance,
    send_message_user,
)
from bot_processing.is_valid import format_phone, is_valid_phone_number
from bot_processing.work_exls import add_form_excl_doc
from pg.pg_query import (
    check_user_in_flags,
    clear_pre_order,
    get_data_in_table,
    get_last_id_order,
    save_data_in_table_orders,
    save_data_in_table_pre_order_one,
    save_data_in_table_users_one,
    save_data_pre_order,
    update_flag_in_table_flags,
)


TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)


async def place_an_order(chat_id):
    '''Запрос у пользователя на ввод ФИО'''
    res = check_user_in_flags(chat_id)
    print(res)
    update_flag_in_table_flags(chat_id, "EnterFIO")
    text = """Введите Ваше ФИО"""
    # keyboard = (keyboard_answers_to_popular_questions())
    await send_message_user(chat_id, text)


async def add_fio(fio, chat_id, tg_name):
    '''Сохранение ФИО и имени пользователя в БД и запрос номера телефона'''
    save_data_in_table_users_one("fio", fio, chat_id)
    save_data_in_table_users_one("tg_name", tg_name, chat_id)
    update_flag_in_table_flags(chat_id, "EnterPhone")
    text = "Введите номер телефона:"
    await get_phone(chat_id, text)


async def add_phone(phone, chat_id):
    '''Сохранение номера телефона в БД и запрос направления доставки'''
    phone = is_valid_phone_number(phone)
    if phone is False:
        text = "Не могу разобрать ваш номер телефона, повторите ввод или нажмите 'Поделится номером телефона':"
        await get_phone(chat_id, text)
    else:
        update_flag_in_table_flags(chat_id, None)
        phone = format_phone(phone)
        save_data_in_table_users_one("phone", phone, chat_id)
        # last_id = get_last_id_order()
        # id_order = int(last_id[0])+1

        update_flag_in_table_flags(chat_id, "EnterDeliveryDirection")
        text = "Выберите направление доставки"
        await send_message_user(chat_id, text, keyboard=keyboard_delivery_direction())


async def add_delivery_direction(chat_id, city):
    '''Сохранение направления доставки в БД и запрос на добавление страховки'''
    update_flag_in_table_flags(chat_id, None)
    save_data_pre_order(chat_id, city)
    text = "Нужна ли страховка?"
    await send_message_user(chat_id, text, keyboard=keyboard_insurance())


async def add_insurance(chat_id, answer, flag=True):
    '''Сохранение ответа на вопрос о страховке в БД и запрос ссылки на товар'''
    if flag:
        save_data_in_table_pre_order_one("insurance", answer, chat_id)
    else:
        await save_order(chat_id)
        save_data_in_table_pre_order_one("link_product", None, chat_id)
        save_data_in_table_pre_order_one("img_product", None, chat_id)
        save_data_in_table_pre_order_one("img_color", None, chat_id)
        save_data_in_table_pre_order_one("img_size", None, chat_id)
        save_data_in_table_pre_order_one("count", None, chat_id)
        save_data_in_table_pre_order_one("price", None, chat_id)
        save_data_in_table_pre_order_one("amount", None, chat_id)
    update_flag_in_table_flags(chat_id, "Link_product")
    text = "Вставьте ссылку на товар:"
    await send_message_user(chat_id, text)


async def save_order(chat_id):
    '''Сохранение заказа в БД и запрос на добавление товара'''
    order_data = await get_data_in_table("pre_order", "chat_id", chat_id)
    print("order_data", order_data)

    if order_data.get("id_order") is None:
        last_id = get_last_id_order()
        print("last_id", last_id)
        id_order = int(last_id[0]) + 1
        save_data_in_table_pre_order_one("id_order", id_order, chat_id)
        await save_data_in_table_orders(order_data, id_order, chat_id)
    else:
        await save_data_in_table_orders(order_data, order_data.get("id_order"), chat_id)


async def save_order_end(chat_id):
    '''Сохранение заказа в БД и запрос на добавление товара'''
    order_data = await get_data_in_table("pre_order", "chat_id", chat_id)
    if order_data.get("id_order") is None:
        last_id = get_last_id_order()
        id_order = int(last_id[0]) + 1
        await save_data_in_table_orders(order_data, id_order, chat_id)
    else:
        id_order = order_data.get("id_order")
        await save_data_in_table_orders(order_data, order_data.get("id_order"), chat_id)

    await clear_pre_order(chat_id)
    res = await add_form_excl_doc(chat_id, id_order)
    if res:
        text = f"Ваш заказ успешно создан: {res} "
        await send_message_user(chat_id, text)
    else:
        text = "Заказ не сформирован"
        await send_message_user(chat_id, text)


async def add_link_product(chat_id, link):
    '''Сохранение ссылки на товар в БД и запрос на добавление фото товара'''
    save_data_in_table_pre_order_one("link_product", link, chat_id)
    update_flag_in_table_flags(chat_id, "Img_product")
    text = "Вставьте скрин товара:"
    await send_message_user(chat_id, text)


async def add_Img_product(chat_id, file_id, file_unique_id):
    '''Сохранение фото товара в БД и запрос на добавление фото цвета товара'''
    update_flag_in_table_flags(chat_id, "Img_color")
    print("file_unique_id", file_unique_id)
    parent_dir = "data/link_product"
    path = os.path.join(parent_dir, f"{chat_id}")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Папка создана: {path}")
    else:
        print(f"Папка уже существует: {path}")

    photo_file = await bot.get_file(file_id)
    extension = photo_file.file_path.split(".")[-1].lower()
    print(f"Расширение файла: {extension}")
    filename = f"{file_unique_id}.{extension}"
    save_path = os.path.join(path, filename)
    await photo_file.download_to_drive(save_path)
    save_data_in_table_pre_order_one("img_product", save_path, chat_id)
    text = "Вставьте скрин цвета товара:"
    await send_message_user(chat_id, text)


async def add_Img_color(chat_id, file_id, file_unique_id):
    '''Сохранение фото цвета товара в БД и запрос на добавление фото размера товара'''
    update_flag_in_table_flags(chat_id, "Img_size")
    print("file_unique_id", file_unique_id)
    parent_dir = "data/link_product"
    path = os.path.join(parent_dir, f"{chat_id}")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Папка создана: {path}")
    else:
        print(f"Папка уже существует: {path}")

    photo_file = await bot.get_file(file_id)
    extension = photo_file.file_path.split(".")[-1].lower()
    print(f"Расширение файла: {extension}")
    filename = f"{file_unique_id}.{extension}"
    save_path = os.path.join(path, filename)
    await photo_file.download_to_drive(save_path)
    save_data_in_table_pre_order_one("img_color", save_path, chat_id)
    text = "Вставьте скрин размера товара:"
    await send_message_user(chat_id, text)


async def add_Img_size(chat_id, file_id, file_unique_id):
    '''Сохранение фото размера товара в БД и запрос на добавление количества товара'''
    update_flag_in_table_flags(chat_id, "Count_product")
    print("file_unique_id", file_unique_id)
    parent_dir = "data/link_product"
    path = os.path.join(parent_dir, f"{chat_id}")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Папка создана: {path}")
    else:
        print(f"Папка уже существует: {path}")

    photo_file = await bot.get_file(file_id)
    extension = photo_file.file_path.split(".")[-1].lower()
    print(f"Расширение файла: {extension}")
    filename = f"{file_unique_id}.{extension}"
    save_path = os.path.join(path, filename)
    await photo_file.download_to_drive(save_path)
    save_data_in_table_pre_order_one("img_size", save_path, chat_id)

    text = "Количество товара:"
    await send_message_user(chat_id, text)


async def add_count_product(chat_id, count):
    '''Сохранение количества товара в БД и запрос на добавление цены товара'''
    update_flag_in_table_flags(chat_id, "Price_product")
    print("count", count)
    print("count", type(count))
    save_data_in_table_pre_order_one("count", int(count), chat_id)

    text = "Укажите стоимость товара в юанях за 1 штуку:"
    await send_message_user(chat_id, text)


async def add_price_product(chat_id, count):
    '''Сохранение цены товара в БД и запрос на добавление товара'''
    save_data_in_table_pre_order_one("price", float(count), chat_id)
    update_flag_in_table_flags(chat_id, "Price_product")

    text = "Товар добавлен в корзину, хотите добавить еще один товар?"
    await send_message_user(chat_id, text, keyboard=keyboard_add_product())
