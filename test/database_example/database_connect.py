import psycopg2 as pg2

conn = pg2.connect(
    host="localhost",
    database="spotify",
    port="5432",
    user="postgres",
    password="re64postgre"
)

cursor = conn.cursor()
cursor.execute("select * from users")
results = cursor.fetchall()

for row in results:
    print(row)

conn.commit()
cursor.close()
conn.close()