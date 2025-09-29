

from bot_processing.func import keyboard_to_popular_questions_and_back, send_message_user
from services.сurrency_course import get_currency_course



async def cost_calculator(chat_id):
    '''Отправляет пользователю ответ на вопрос "Как рассчитать стоимость доставки?"'''
    #Получать курс юаня к рублю
    course = get_currency_course()
    # print(course)
    text = (
        f"""🌟 *СКОРО ГРЯДЕТ КРУТОЕ ОБНОВЛЕНИЕ!* 🌟

Следите за новостями, чтобы не пропустить! 

📅 Курс на сегодня: {course}""")
    keyboard = keyboard_to_popular_questions_and_back()
    await send_message_user(chat_id, text, keyboard)