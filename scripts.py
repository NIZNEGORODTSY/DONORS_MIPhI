import re
import datetime


def is_valid_russian_phone(phone):
    pattern = r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    return bool(re.fullmatch(pattern, phone))


def compare_date(date1: datetime.date, date2: datetime.date):
    today = datetime.date.today()
    if date1 != 0 & date2 != 0:
        delta1 = abs((today.days() - date1.days))
        delta2 = abs((today.days() - date2.days))
        if delta1 < delta2:
            return date1, 'Центр Крови им. О.К. Гаврилова'
        else:
            return date2, 'Центр Крови ФМБА'
    return 0, 'Невозможно загрузить данные'
