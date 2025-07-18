import re
import datetime


def is_valid_russian_phone(phone):
    pattern = r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    return bool(re.fullmatch(pattern, phone))


def compare_date(date1: datetime.date, date2: datetime.date):
    today = datetime.date.today()
    try:
        if date1 != 0 or date2 != 0:
            delta1 = abs((date1 - today).days)
            delta2 = abs((date2 - today).days)
            if delta1 < delta2:
                return date1, 'Центр Крови им. О.К. Гаврилова'
            else:
                return date2, 'Центр Крови ФМБА'
    except Exception:
        return 0, Exception


def display_history(data):
    places = {"FMBA": "Центр Крови ФМБА", "Gavr": "Центр Крови им. О.К. Гаврилова"}
    cnt = 0
    res = ''
    for donation in data:
        date = donation.DonDate
        place = donation.DonPlace
        number = cnt + 1
        res += f"{number}: {date}, {places[place]}\n"
    return res
