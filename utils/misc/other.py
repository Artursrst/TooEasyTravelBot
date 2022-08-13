import re

def is_float(string:str) -> bool or str:
    '''
    Функция для проверки является ли строка числом формата float

    :param string: строка, которую нужно проверить
    :return: string or False
    '''
    check = re.match(r'\d*\.?\d+', string)
    if check:
        return check.group() == string
    return False