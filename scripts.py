import re
import datetime
import requests


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


def validate_full_name(full_name):
    if not isinstance(full_name, str):
        return False

    pattern = r'^[А-ЯЁ][а-яё-]+ [А-ЯЁ][а-яё-]+ [А-ЯЁ][а-яё-]+$'

    if not re.fullmatch(pattern, full_name):
        return False

    parts = full_name.split()
    for part in parts:
        if part.startswith('-') or part.endswith('-') or '--' in part:
            return False

    return True


# Координаты Москвы
LATITUDE = 55.7558
LONGITUDE = 37.6176


def get_location_by_ip():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        loc = data.get('loc', 'N/A')
        return loc
    except Exception as e:
        print(f"Ошибка: {e}")


def get_daily_weather():
    LATITUDE, LONGITUDE = get_location_by_ip()
    """Получает погоду в Москве на сегодня."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Moscow",
        "forecast_days": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Ошибка: Не удалось получить данные (код {response.status_code})")
        return None

    return response.json()


def generate_donor_advice(weather_data) -> str:
    """Генерирует персонализированные советы для доноров на основе погоды."""
    if not weather_data:
        return "Не удалось получить данные о погоде. Пожалуйста, следуйте общим рекомендациям."

    current = weather_data.get("current", {})
    temp = current.get("temperature_2m", 20)
    humidity = current.get("relative_humidity_2m", 50)
    wind = current.get("wind_speed_10m", 5)
    precipitation = current.get("precipitation", 0)

    advice = "🌤 Рекомендации для доноров на сегодня:\n\n"

    # Температурные советы
    if temp > 25:
        advice += "☀️ Жарко! Пейте 2-3 литра воды до донации и избегайте солнца.\n"
    elif temp < 10:
        advice += "❄️ Холодно! Оденьтесь теплее и пейте тёплые напитки.\n"
    else:
        advice += "✅ Идеальная температура для сдачи крови.\n"

    # Советы по влажности
    if humidity < 40:
        advice += "💧 Сухой воздух — увеличьте потребление воды.\n"
    elif humidity > 80:
        advice += "🌫 Высокая влажность — возможна быстрая утомляемость.\n"

    # Советы по ветру
    if wind > 15:
        advice += "🌬 Сильный ветер — возьмите ветровку.\n"

    # Советы по осадкам
    if precipitation > 0:
        advice += "☔️ Ожидаются осадки — возьмите зонт.\n"

    # Общие универсальные советы
    advice += "\nОбщие рекомендации:\n"
    advice += "🍎 Поешьте за 2 часа до сдачи (гречка, печень, яблоки)\n"
    advice += "💤 Хорошо выспитесь накануне (не менее 7-8 часов)\n"
    advice += "🧂 Избегайте солёной и жирной пищи перед донацией\n"
    advice += "🧦 Наденьте удобную одежду с короткими рукавами\n"
    advice += "🕒 Запланируйте отдых 30-40 минут после процедуры"

    return advice


def display_weather(data):
    """Выводит погоду и рекомендации."""
    if not data:
        print("Нет данных о погоде")
        return

    current = data.get("current", {})
    print("\n=== Погода в Москве на сегодня ===")
    print(f"Температура: {current.get('temperature_2m')}°C")
    print(f"Влажность: {current.get('relative_humidity_2m')}%")
    print(f"Ветер: {current.get('wind_speed_10m')} км/ч")
    print(f"Осадки: {current.get('precipitation')} мм")

    print("\n" + generate_donor_advice(data))
