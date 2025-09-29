# from pg.pg_con import dbConnection
# from pg.pg_query import save_data_in_table_users #get_data_table_where
import telegram
# from telegram import BotCommand
import os

# db = dbConnection()

TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)


# def start_massages(data):
#     message_dict = data.get("message")
#     chat_dict = message_dict.get("chat")

#     username = chat_dict.get("username")
#     chat_id = chat_dict.get("id")
#     first_name = chat_dict.get("first_name")

#     columns = ["chat_id", "username", "first_name"]
#     try:
#         # Сохраняем данные в БД, если пользователь есть в БД запись не произойдет
#         # db.execute(save_data_in_table_users(columns, chat_id, username, first_name))
#         return True
#     except Exception as ex:
#         print("Ошибка", ex)
#         return False


async def show_menu_registered_user(chat_id):
    '''Отправляет пользователю стартовое сообщение с кнопками и фото'''
    main_menu_commands = [
        telegram.BotCommand(command="/start", description="Перезапустить бота"),
        telegram.BotCommand(command="/help", description="Популярные вопросы"),
        telegram.BotCommand(command="/calculator", description="Калькулятор"),
    ]
    await bot.set_my_commands(
        main_menu_commands, scope=telegram.BotCommandScopeChat(chat_id=chat_id)
    )


