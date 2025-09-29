import asyncio
import os
import telegram


TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(TOKEN)


async def bot_register_url():
    '''Регистрация URL для вебхука бота'''
    async with bot:
        # print(await bot.get_me())
        return await bot.setWebhook("https://chinayiwu-ludmila.amvera.io/bot")
    asyncio.run(main())  # noqa: F821
