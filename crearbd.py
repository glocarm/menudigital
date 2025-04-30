from conectar import obtener_conexion

# Obtener la conexión
conn = obtener_conexion()
cursor=conn.cursor()

if conn.is_connected():
    print("Conexión exitosa a la base de datos.")
    # Crear la tabla CATEGORIA
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categoria(
        idcategoria INTEGER PRIMARY KEY,
        nombrecat VARCHAR(200)
    )
    ''')
    
    # Crear la tabla MENU
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu(
        idmenu INTEGER PRIMARY KEY,
        nombremenu VARCHAR(200),
        descrimenu VARCHAR(200),
        preciomenu FLOAT,
        urlimg VARCHAR(150),
        idcategoria INTEGER NOT NULL,
                    FOREIGN KEY (idcategoria) REFERENCES categoria(idcategoria)  
    )
    ''')
        
conn.commit()
conn.close()
