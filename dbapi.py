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


def add_user(number: str, tgid: int):
    def my_query(cursor):
        query = f"""INSERT INTO users (phonenumber, tgid, isadmin) VALUES ('{number}', '{tgid}', 0)"""
        cursor.execute(query)

    execute(my_query)


def add_fio(tgid: int, fio: str):
    def my_query(cursor):
        query = f"""UPDATE users SET fio = '{fio}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)

    execute(my_query)


def add_ugroup(tgid: int, ugroup: str):
    def my_query(cursor):
        query = f"""UPDATE users SET ugroup = '{ugroup}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)

    execute(my_query)


def add_contacts(tgid: int, contacts: str):
    def my_query(cursor):
        query = f"""UPDATE users SET contacts = '{contacts}' WHERE tgid = '{tgid}'"""
        cursor.execute(query)

    execute(my_query)


def add_donation(uid: int):
    def my_query(cursor):
        query = f"""INSERT INTO donations (uid) VALUES ({uid})"""
        cursor.execute(query)

    execute(my_query)


def add_donation_donplace(uid: int, donplace: int):
    def my_query(cursor):
        query = f"""UPDATE donations SET donplace = {donplace} WHERE uid = {uid}"""
        cursor.execute(query)

    execute(my_query)


def add_donation_donplace(uid: int, dondate: str):
    def my_query(cursor):
        query = f"""UPDATE donations SET dondate = '{dondate}' WHERE uid = {uid}"""
        cursor.execute(query)

    execute(my_query)


def get_user(tgid: int) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE tgid = '{tgid}'"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def get_donation_history(uid: int) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM donations WHERE uid = {uid} ORDER BY dondate"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def get_admins() -> list:
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
        query = f"""INSERT INTO questions (uid, question, hasreply, isseen) VALUES ({uid}, '{question}', 0, 0)"""
        cursor.execute(query)

    execute(my_query)


def get_all_questions() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM questions ORDER BY id_q"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def get_upcoming_events() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM upcoming_event"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def add_question_ans(qid: int, ans: str):
    def my_query(cursor):
        query = f"""UPDATE questions SET answer = '{ans}' WHERE id_q = {qid}"""
        cursor.execute(query)

    execute(my_query)


def add_question_repl_cond(qid: int):
    def my_query(cursor):
        query = f"""UPDATE questions SET hasreply = 1 WHERE id_q = {qid}"""
        cursor.execute(query)

    execute(my_query)

def add_question_isseen_cond(uid: int):
    def my_query(cursor):
        query = f"""UPDATE questions SET isseen = 1 WHERE uid = {uid}"""
        cursor.execute(query)

    execute(my_query)


def add_registration(eid: int, uid: int):
    def my_query(cursor):
        query = f"""INSERT INTO registered_people (id_events, uid) VALUES ({eid}, {uid})"""
        cursor.execute(query)

    execute(my_query)


def get_all_users() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users"""


def get_donor(phone_number: int) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE tgid = '{phone_number}'"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res


def edit_donor(rules: dict, phone_number: str):
    def my_query(cursor):
        for key, value in rules.items():
            query = f"""UPDATE users SET '{key}' = '{value}' WHERE phonenumver = '{phone_number}'"""
            cursor.execute(query)

    execute(my_query)


def get_questions_by_user(uid: int):
    def my_query(cursor):
        query = f"""SELECT * FROM questions WHERE uid = {uid}"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res

def get_all_registrations() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM registered_people"""
        cursor.execute(query)
        return cursor.fetchall()
    res = execute(my_query)
    return res

def get_all_users() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users"""
        cursor.execute(query)
        return cursor.fetchall()
    res = execute(my_query)
    return res

def get_all_donations() -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM donations"""
        cursor.execute(query)
        return cursor.fetchall()
    res = execute(my_query)
    return res


def get_donor(phone_number: int) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE tgid = '{phone_number}'"""
        cursor.execute(query)
        return cursor.fetchall()

    res = execute(my_query)
    return res
