import sqlite3

conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()

cursor.execute('SELECT *  FROM menu')

filas = cursor.fetchall()

for fila in filas: 
    print(fila)

conn.close()