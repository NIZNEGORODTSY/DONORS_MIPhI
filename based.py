import mysql.connector

# Establish connection
connection = mysql.connector.connect(
      host='192.168.0.108',
      user='gg_user',
      password='1234',
      database='db'
)

# Create a cursor object
cursor = connection.cursor()

# Execute a query


def gets_admins():
    a=[]
    cursor.execute("SELECT * FROM tb1")
    results = cursor.fetchall()
    for row in results:
       a.append(row[1])
    return a
