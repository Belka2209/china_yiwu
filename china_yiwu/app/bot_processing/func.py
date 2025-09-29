import telegram

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import os


TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)


async def get_phone(chat_id, text):
    '''Кнопка: запрос номера телефона у пользователя'''
    button = KeyboardButton("Поделиться номером телефона", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(
        [[button]], resize_keyboard=True, one_time_keyboard=True, is_persistent=False
    )
    await bot.send_message(chat_id, text, reply_markup=reply_markup)


def keyboard_repeat_phone_or_unregistered_user():
    """Кнопки: для повторного ввода номера телефона или войти как незарегистрированный пользователь"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Ввести номер телефона",
                    callback_data="Repeat_enter_phone",
                )
            ],
            [
                InlineKeyboardButton(
                    # "Авторизоваться как незарегистрированный пользователь",
                    "Зарегистрироваться",
                    callback_data="Log_in_as_an_unregistered_user",
                )
            ],
        ]
    )
    return reply_markup


def keyboard_start_message():
    """Кнопки: стартового сообщения"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🛒 Оформить заказ",
                    callback_data="Place_an_order",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🧮 Калькулятор стоимости",
                    callback_data="Cost_calculator",
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ Отзывы о нашей работе",
                    url="https://t.me/china_yiwu",
                    callback_data="Reviews_about_our_work",
                )
            ],
            [
                InlineKeyboardButton(
                    "❓ Ответы на популярные вопросы",
                    callback_data="Answers_to_popular_questions",
                )
            ],
            [
                InlineKeyboardButton(
                    "📦 Отследить посылку",
                    callback_data="Track_the_parcel",
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Задать вопрос",
                    callback_data="Ask_a_question",
                )
            ],
            [
                InlineKeyboardButton(
                    "👨‍💼 Заказ от оператора",
                    callback_data="Order_from_the_operator",
                )
            ],
            [
                InlineKeyboardButton(
                    "📱 Скачать POIZON iOS",
                    callback_data="ios",
                )
            ],
            [
                InlineKeyboardButton(
                    "📲 Скачать POIZON Android",
                    callback_data="Android",
                )
            ],
        ]
    )
    return reply_markup


def keyboard_answers_to_popular_questions():
    '""Кнопки: ответы на популярные вопросы"""'
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    """🛍 Будет ли цена дешевле, \r\n если заказать несколько вещей?""",
                    callback_data="Will_the_price_be_cheaper",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Какая у Вас комиссия?",
                    callback_data="What_is_your_commission",
                )
            ],
            [
                InlineKeyboardButton(
                    "🚛 Какой срок доставки?",
                    callback_data="What_is_the_delivery_time",
                )
            ],
            [
                InlineKeyboardButton(
                    "🌍 В какие страны доставляем?",
                    callback_data="What_countries_do_we_deliver",
                )
            ],
            [
                InlineKeyboardButton(
                    "Что делать, если пришел бракованный товар?",
                    callback_data="Defective_product",
                )
            ],
            [
                InlineKeyboardButton(
                    "Почему товар пришел без пломб и с сертификатом без QR-кода?",
                    callback_data="Without_seals_and_certificate",
                )
            ],
            [
                InlineKeyboardButton(
                    "Как отследить мой заказ?",
                    callback_data="How_to_track_my_order",
                )
            ],
            [
                InlineKeyboardButton(
                    "Как правильно подобрать размер?",
                    callback_data="Pick_up_the_size",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔍 Не нашли нужную категорию товара?",
                    callback_data="Not_find_the_desired_category_of_goods",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Вернуться в меню",
                    callback_data="Return_to_the_menu",
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         "📱 Скачать POIZON iOS",
            #         callback_data="ios",
            #     )
            # ],
            # [
            #     InlineKeyboardButton(
            #         "📲 Скачать POIZON Android",
            #         callback_data="Android",
            #     )
            # ],
        ]
    )
    return reply_markup


def keyboard_to_popular_questions_and_back():
    """Кнопки: ответы на популярные вопросы и вернуться в меню"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❓ Ответы на популярные вопросы",
                    callback_data="Answers_to_popular_questions",
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться в меню",
                    callback_data="Start_message",
                )
            ],
        ]
    )
    return reply_markup


async def send_message_user(chat_id, text, keyboard=None):
    """Отправляет сообщение пользователю с кнопками"""
    await bot.send_message(
        chat_id, text=text, reply_markup=keyboard, parse_mode="Markdown"
    )


def keyboard_delivery_direction():
    """Кнопки: направления доставки"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Москва",
                    callback_data="Direction_moscow",
                )
            ],
            [
                InlineKeyboardButton(
                    "Уссурийск",
                    callback_data="Direction_ussuriysk",
                )
            ],
            [
                InlineKeyboardButton(
                    "Казахстан",
                    callback_data="Direction_kazakhstan",
                )
            ],
        ]
    )
    return reply_markup


def keyboard_insurance():
    """Кнопки: нужна ли страховка"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Да",
                    callback_data="Insurance_yes",
                )
            ],
            [
                InlineKeyboardButton(
                    "Нет",
                    callback_data="Insurance_no",
                )
            ],
        ]
    )
    return reply_markup


def keyboard_add_product():
    """Кнопки: добавить товар или завершить заказ"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Да",
                    callback_data="Add_product_yes",
                )
            ],
            [
                InlineKeyboardButton(
                    "Нет",
                    callback_data="Add_product_no",
                )
            ],
        ]
    )
    return reply_markup


