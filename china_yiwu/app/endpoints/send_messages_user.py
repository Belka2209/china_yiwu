from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import os
import dotenv
import telegram

dotenv.load_dotenv()
getenv = os.getenv


TOKEN = getenv("TG-TOKEN")

bot = telegram.Bot(TOKEN)


async def send_messages_user(request: Request):
    '''Отправляет сообщение пользователю по его ID и тексту сообщения'''
    data = await request.json()
    print("data", data)
    chat_id = data.get("chat_id")
    text = data.get("message")

    try:
        await bot.send_message(chat_id, text)
        return JSONResponse(
            status_code=200,
            content={
                "success": f"Сообщение отправлено пользователю {chat_id}",
            },
        )
    except Exception as ex:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Сообщение не отправлено: ", ex)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
        result = {"error": f"{ex}"}
        raise HTTPException(status_code=500, detail=result)
