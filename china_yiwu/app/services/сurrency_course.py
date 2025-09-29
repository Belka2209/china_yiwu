import requests
import os
from datetime import date

from pg.pg_query import get_course, save_data_in_course
# from fastapi import Request
TOKEN = os.getenv("EXCHANGERATE_API")
# TOKEN = "8977f9c995912247bc0e89ea"

def get_currency_course():
    '''Получение курса валюты'''
    today = date.today()
    res = get_course(today)
    if res is None:
        print("Сделай запись в БД")
        url = f'https://v6.exchangerate-api.com/v6/{TOKEN}/latest/CNY'
        response = requests.get(url)
        data = response.json()
        data = data.get("conversion_rates").get("RUB")
        save_data_in_course(str(today), data)
        get_currency_course()
    else:
        return res

    

    # # Your JSON object
    # print (data.get("conversion_rates").get("RUB"))
    # today = date.today()
    # print(today)  # 2023-11-15
    #Получаю курс валюты ели он есть в БД на сегодня 
    
