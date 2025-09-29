from bot_processing.func import keyboard_start_message
from bot_processing.processing_bot_messages import show_menu_registered_user
import telegram
import os

TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)

async def message_start(chat_id):
    '''Отправляет пользователю стартовое сообщение с кнопками и фото'''
    await bot.send_photo(
        chat_id,
        photo="/data/start_message.jpg",
        caption="""😉*Добро пожаловать в бот группы Panda logicitrics!*

    Наша группа поможет Вам выкупить товары с ЛЮБЫХ китайских площадок, например:
    1⃣ POIZON (DEWU)
    2⃣ taobao.com
    3⃣ и другие.

    ⛔️Все расчеты, заказы и оплата производятся ТОЛЬКО В БОТЕ. Мы не принимаем оплату в личных сообщениях!⛔️

    ⚠️ Товар возврату и обмену не подлежит. Мы оказываем услуги только выкупа и доставки товаров.""",
        reply_markup=keyboard_start_message(),
        parse_mode='Markdown'
    )
    await show_menu_registered_user(chat_id)
