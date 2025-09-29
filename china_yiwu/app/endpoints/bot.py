# import sys
from bot_processing.callback_query.place_an_order import (
    add_Img_color,
    add_Img_product,
    add_Img_size,
    add_count_product,
    add_delivery_direction,
    add_fio,
    add_insurance,
    add_link_product,
    add_phone,
    add_price_product,
    place_an_order,
    save_order_end,
)
from bot_processing.callback_query.cost_calculator import cost_calculator
from bot_processing.callback_query.android import android
from bot_processing.callback_query.answers_to_popular_questions import (
    answers_to_popular_questions,
    defective_product,
    how_to_track_my_order,
    not_find_the_desired_category_of_goods,
    pick_up_the_size,
    what_countries_do_we_deliver,
    what_is_the_delivery_time,
    what_is_your_commission,
    will_the_price_be_cheaper,
    without_seals_and_certificate,
)
from bot_processing.callback_query.ask_a_question import ask_a_question

from bot_processing.callback_query.ios import ios
from bot_processing.callback_query.order_from_the_operator import (
    order_from_the_operator,
)
from bot_processing.callback_query.reviews_about_our_work import reviews_about_our_work
from bot_processing.callback_query.track_the_parcel import track_the_parcel

from bot_processing.work_exls import add_form_excl_doc
from pg.pg_query import (
    add_tables_task,
    check_user_in_flags,
    save_data_in_tasks,
    update_flag_in_table_flags,
)

# from endpoints.message_calculator import message_calculator
import telegram

from loguru import logger
from bot_processing.message_start import message_start
import os

# import dotenv
# dotenv.load_dotenv()
from fastapi import Request
from pg.pg_con import dbConnection

db = dbConnection()
TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)
logger.add(
    "file_1.log", level="INFO", format="{time} {level} {message}", rotation="500 MB"
)
# logger.add(sys.stderr, format="{time} {level} {message}", filter="sub.module", level="INFO")

# info_user = {}


async def main_bot(request: Request):
    '''Обработка сообщений от пользователей'''
    # print("hello")
    req = await request.json()
    print("req", req)

    async with bot:
        # try:
            if req.get("message") is not None:
                chat_id = req.get("message").get("chat").get("id")
                flag = check_user_in_flags(chat_id)
                print("flag", flag)
                print("chat_id", chat_id)
                if req.get("message").get("contact") is None:
                    message = req.get("message").get("text")
                    photo = req.get("message").get('photo')
                    if photo is not None:
                        file_id = req['message']['photo'][-1]['file_id']
                        file_unique_id = req['message']['photo'][-1]['file_unique_id']
                    print("photo", photo)
                    print("message", message)
                    if message == "/start":
                        update_flag_in_table_flags(chat_id, None)
                        save_data_in_tasks("start_enter", chat_id)
                        await message_start(chat_id)
                    elif message == "/help":
                        await answers_to_popular_questions(chat_id)
                    elif message == "/calculator":
                        await cost_calculator(chat_id)
                    elif message == "/db":
                        db.execute(add_tables_task())
                    elif message is not None and flag == "EnterFIO":
                        tg_name = f'@{req.get("message").get("chat").get('username')}'
                        await add_fio(message, chat_id, tg_name)
                    elif message is not None and flag == "Link_product":
                        await add_link_product(chat_id, message)
                    elif (message is None and photo is not None) and flag == "Img_product":
                        await add_Img_product(chat_id, file_id, file_unique_id)
                    elif (message is None and photo is not None) and flag == "Img_color":
                        await add_Img_color(chat_id, file_id, file_unique_id)
                    elif (message is None and photo is not None) and flag == "Img_size":
                        await add_Img_size(chat_id, file_id, file_unique_id)
                    elif message == "n":
                        await add_form_excl_doc(chat_id, 4)

                    elif (
                        req.get("message").get("text") is not None
                        and flag == "EnterPhone"
                    ):
                        await add_phone(message, chat_id)
                    elif (
                        req.get("message").get("text") is not None
                        and flag == "Count_product"
                    ):
                        await add_count_product(chat_id, message)
                    elif (
                        req.get("message").get("text") is not None
                        and flag == "Price_product"
                    ):
                        await add_price_product(chat_id, message)

                    else:
                        await bot.send_message(
                            chat_id,
                            text=f"Мне очень нравится твое сообщение: {message}, \n Но я еще не могу на него ответить",
                        )
                elif req.get("message").get("contact") is not None and flag is not None:
                    if flag == "EnterPhone":
                        phone = req.get("message").get("contact").get("phone_number")
                        await add_phone(phone, chat_id)

            #  18
            if req.get("callback_query") is not None:
                chat_id = req.get("callback_query").get("from").get("id")
                callback_query = req.get("callback_query").get("data")
                #  {#c62,18}
                if callback_query == "Place_an_order":
                    save_data_in_tasks("users", chat_id)
                    update_flag_in_table_flags(chat_id, None)
                    await place_an_order(chat_id)
                elif callback_query == "Direction_moscow":
                    await add_delivery_direction(chat_id, "Москва")
                elif callback_query == "Direction_ussuriysk":
                    await add_delivery_direction(chat_id, "Уссурийск")
                elif callback_query == "Direction_kazakhstan":
                    await add_delivery_direction(chat_id, "Казахстан")
                elif callback_query == "Insurance_yes":
                    await add_insurance(chat_id, True)
                elif callback_query == "Insurance_no":
                    await add_insurance(chat_id, False)
                elif callback_query == "Add_product_yes":
                    await add_insurance(chat_id, None, False)
                elif callback_query == "Add_product_no":
                    await save_order_end(chat_id)
                elif callback_query == "Cost_calculator":
                    await cost_calculator(chat_id)
                elif callback_query == "Reviews_about_our_work":
                    await reviews_about_our_work(chat_id)
                elif callback_query == "Answers_to_popular_questions":
                    await answers_to_popular_questions(chat_id)
                elif callback_query == "Track_the_parcel":
                    await track_the_parcel(chat_id)
                elif callback_query == "Ask_a_question":
                    await ask_a_question(chat_id)
                elif callback_query == "Order_from_the_operator":
                    await order_from_the_operator(chat_id)
                elif callback_query == "ios":
                    await ios(chat_id)
                elif callback_query == "Android":
                    await android(chat_id)
                elif callback_query == "Will_the_price_be_cheaper":
                    await will_the_price_be_cheaper(chat_id)
                elif callback_query == "What_is_your_commission":
                    await what_is_your_commission(chat_id)
                elif callback_query == "What_is_the_delivery_time":
                    await what_is_the_delivery_time(chat_id)
                elif callback_query == "Start_message":
                    await message_start(chat_id)
                elif callback_query == "What_countries_do_we_deliver":
                    await what_countries_do_we_deliver(chat_id)
                elif callback_query == "Defective_product":
                    await defective_product(chat_id)
                elif callback_query == "Without_seals_and_certificate":
                    await without_seals_and_certificate(chat_id)
                elif callback_query == "How_to_track_my_order":
                    await how_to_track_my_order(chat_id)
                elif callback_query == "Pick_up_the_size":
                    await pick_up_the_size(chat_id)
                elif callback_query == "Not_find_the_desired_category_of_goods":
                    await not_find_the_desired_category_of_goods(chat_id)
                elif callback_query == "Return_to_the_menu":
                    await message_start(chat_id)
        # except Exception as ex:
        #     print("Ошибка", ex)
   