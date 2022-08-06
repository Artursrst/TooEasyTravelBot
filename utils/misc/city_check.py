import string

def city_ch(city_name:str) -> bool:
    '''
    Функция для проверки введённый пользователем информации, на этапе выбора города, заданным критериям

    :param city_name: город отправленный пользователем
    :return: True or False
    :rtype: bool
    '''

    for l in city_name:
        if l not in string.ascii_letters and l not in ' ':
            return False

    return True