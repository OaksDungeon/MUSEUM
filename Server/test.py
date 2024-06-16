import psycopg2


conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM events")
events_mas = cursor.fetchall()
print(events_mas[1][1])
cursor.close() 
conn.close()