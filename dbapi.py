import psycopg2
import config.reader as reader

reader.read_config()


def execute(dbfun):
    conn = psycopg2.connect(
        # dbname=reader.get_param_value('dbname'),
        user=reader.get_param_value('dbuser'),
        password=reader.get_param_value('dbpwd'),
        host=reader.get_param_value('dbhost'),
        port=reader.get_param_value('dbport')
    )

    cursor = conn.cursor()
    res = dbfun(cursor)
    conn.commit()
    conn.close()
    return res


# Шаблон
def some_function():
    def my_query(cursor):
        query = f"""some query"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def get_users_gy_phone(phone: str) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE PhoneNumber = '{phone}'"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def get_uid(tgid: int):
    def my_query(cursor):
        query = f"""SELECT id FROM users WHERE tgid = '{tgid}'"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def get_admin(tgid: int):
    def my_query(cursor):
        query = f"""SELECT isadmin FROM users WHERE tgid = '{tgid}'"""
        cursor.execute(query)
        return cursor.fetchone()  # Какой-нибудь fetch

    res = execute(my_query)
    return res


def add_user(number: str, tgid: int) -> int:
    def my_query(cursor):
        query = f"""INSERT INTO users (phonenumber, tgid, isadmin) VALUES ('{number}', '{tgid}', 0)"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def add_fio(tgid: int, fio: str) -> int:
    def my_query(cursor):
        query = f"""UPDATE users SET fio = '{fio}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)

    execute(my_query)


def add_ugroup(tgid: int, ugroup: str) -> int:
    def my_query(cursor):
        query = f"""UPDATE users SET ugroup = '{ugroup}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)

    execute(my_query)


def add_contacts(tgid: int, contacts: str) -> int:
    def my_query(cursor):
        query = f"""UPDATE users SET contacts = '{contacts}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def add_donation(uid: int) -> int:
    def my_query(cursor):
        query = f"""INSERT INTO donations (uid) VALUES ({uid})"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def add_donation_donplace(uid: int, donplace: int) -> int:
    def my_query(cursor):
        query = f"""UPDATE donations SET donplace = {donplace} WHERE uid = {uid}"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def add_donation_donplace(uid: int, dondate: str) -> int:
    def my_query(cursor):
        query = f"""UPDATE donations SET dondate = '{dondate}' WHERE uid = {uid}"""
        cursor.execute(query)
        return cursor.fetchone()

    res = execute(my_query)
    return res


def get_user(tgid: int):
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE tgid = '{tgid}'"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def get_donation_history(uid: int):
    def my_query(cursor):
        query = f"""SELECT * FROM donations WHERE uid = {uid} ORDER BY dondate"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res

def get_admins():
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE isadmin = 1"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res

def add_donor(fio: str, ugroup: str, registry: str):
    def my_query(cursor):
        query = f"""INSERT INTO users (fio, ugroup, registry) VALUES ('{fio}', '{ugroup}', '{registry}')"""
        cursor.execute(query)

    execute(my_query)

def add_question(uid: int, question: str):
    def my_query(cursor):
        query = f"""INSERT INTO users (uid, question) VALUES ({uid}, '{question}')"""
        cursor.execute(query)

    execute(my_query)

def get_all_questions() -> list:
    def my_query(cursor):
        query = f"""SLECT * FROM questions"""
        cursor.execute(query)
        return cursor.fetchall()
    res = execute(my_query)
    return res

    execute(my_query)