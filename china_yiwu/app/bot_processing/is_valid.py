
import re


def is_valid_email(email):
    """Функция проверки email на валидность"""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None

def is_valid_inn(inn):
    """Проверка ИНН на валидность"""
    # Убираем пробелы и проверяем длину
    inn = inn.strip()

    if not inn.isdigit() or len(inn) not in [10, 12]:
        return False
    else:
        return True

    # if len(inn) == 10:
    #     # Алгоритм для физ лиц
    #     checksum = sum(int(inn[i]) * (10 - i) for i in range(9)) % 11
    #     if checksum == 10:
    #         checksum = 0
    #     return checksum == int(inn[9])

    # if len(inn) == 12:
    #     # Алгоритм для юр лиц
    #     checksum1 = sum(int(inn[i]) * (2 if i % 2 == 0 else 1) for i in range(10)) % 11
    #     if checksum1 == 10:
    #         checksum1 = 0

    #     checksum2 = sum(int(inn[i]) * (2 if i % 2 == 1 else 1) for i in range(11)) % 11
    #     if checksum2 == 10:
    #         checksum2 = 0

    #     return checksum1 == int(inn[10]) and checksum2 == int(inn[11])

def format_phone(phone_number: str) -> str:
    """Преобразование номера по формату"""
    phone: str = str(phone_number)
    if phone == "nan":
        return ""

    match = re.sub(r"\D", "", phone)
    count_num: int = len(match)

    if count_num == 10:
        # numbers = list(filter(str.isdigit, phone))[:]
        numbers = list(filter(str.isdigit, match))
        return str("+7 {}{}{} {}{}{}-{}{}-{}{}".format(*numbers))
    elif count_num == 11:
        numbers = list(filter(str.isdigit, phone))[1:]
        return str("+7 {}{}{} {}{}{}-{}{}-{}{}".format(*numbers))

    return phone

def is_valid_phone_number(phone_number: str) -> bool:
    """Проверка номера на валидность и убирает все лишние символы"""
    phone_number = "".join(c for c in phone_number if c.isdigit())


    if len(phone_number) == 10:  # Если номер 10 цифр, добавляем код 7
        return format_phone('8' + phone_number) 
    elif len(phone_number) == 11:
        # print(phone_number)
        phone = format_phone(phone_number)
        # print(phone)
        return phone
    else:
        return False

# async def is_valid_password(chat_id, password_user, name_company, first_name):
#     """Проверка пароля"""
#     company_data = get_company_date_is_postg(name_company)
#     if password_user == company_data[3]:
#         if (
#             user_exists(chat_id) is False
#         ):  # Если проверка пароля True, и пользователя нет в БД сохраняем его в БД
#             save_date_user(chat_id, company_data[0], first_name)
#             return True
#         else:
#             if get_user_date_is_postg(chat_id)[1] == company_data[0]:
#                 return True
#             else:
#                 save_date_user(chat_id, company_data[0], first_name)
#                 return True
#     else:
#         return False
