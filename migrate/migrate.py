import psycopg2
import config.reader as reader
import psycopg2
import pandas as pd

reader.read_config()

conn = psycopg2.connect(
        dbname=reader.get_param_value('dbname'),
        user=reader.get_param_value('dbuser'),
        password=reader.get_param_value('dbpwd'),
        host=reader.get_param_value('dbhost'),
        port=reader.get_param_value('dbport')
    )
cursor = conn.cursor()


conn.commit()

conn.close()