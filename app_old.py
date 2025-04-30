import mysql.connector
from flask import Flask, render_template, request,redirect, send_from_directory

# Creamos la conexión con la base de datos:
def obtener_conexion():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurante"
    )
    if conn.is_connected(): 
        print("Conexión exitosa a la base de datos.")
    return conn

def inicio():
    return render_template('restaurante/index.html')