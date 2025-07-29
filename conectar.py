import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurante"
        )
        # Conectar a la base de datos usando mysql.connector
        if conn.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conn
    except:
        print("Error al conectar a la base de datos.")
        return None
obtener_conexion()