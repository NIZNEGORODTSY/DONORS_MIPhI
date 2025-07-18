import psycopg2
import config.reader as reader

reader.read_config()

def some_function():
    def my_query(cursor):
        query = f"""some query"""
        cursor.execute(query)
        return cursor.fetchone() # Какой-нибудь fetch
    res = execute(my_query)
    return res

def get_users_gy_phone(phone: str) -> list:
    def my_query(cursor):
        query = f"""SELECT * FROM users WHERE PhoneNumber={phone}"""
        cursor.execute(query)
        return cursor.fetchall()
    res = execute(my_query)
    return res



def execute(dbfun):
    conn = psycopg2.connect(
        dbname=reader.get_param_value('dbname'),
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