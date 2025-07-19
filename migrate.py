import psycopg2
import config.reader as reader
import os

conn = psycopg2.connect(
    # dbname=reader.get_param_value('dbname'),
    user=reader.get_param_value('dbuser'),
    password=reader.get_param_value('dbpwd'),
    host=reader.get_param_value('dbhost'),
    port=reader.get_param_value('dbport')
)

cursor = conn.cursor()

def migrate_query(filename: str) -> None:
    with open(filename, 'r') as f:
        sql_script = f.read()
    # Удаляем комментарии и лишние пробелы
    cleaned_script = '\n'.join(
        line for line in sql_script.split('\n') 
        if not line.strip().startswith('--')
    )

    # Выполняем каждый запрос отдельно
    for query in cleaned_script.split(';'):
        if query.strip():
            cursor.execute(query)

all_files = os.listdir('migration')

for file in all_files:
    migrate_query('migration/' + file)
    conn.commit()

conn.close()