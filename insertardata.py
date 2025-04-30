from conectar import obtener_conexion

# Obtener la conexión
conn = obtener_conexion()
cursor = conn.cursor()

if conn.is_connected():
    print("Conexión exitosa a la base de datos.")
    # Categorias a insertar
    categorias = [
        (1, 'Bebidas'),
        (2,'Comidas'),
        (3,'Pastelaría'),
        (4,'Panes'),
        (5,'Sin TACC')  
    ]

    # Insertar las categorias del Menú
    cursor.executemany('''
        INSERT INTO categoria (idcategoria, nombrecat)
        VALUES (%s, %s)
    ''', categorias)

    print(f"Se han insertado {cursor.rowcount} registros en la tabla 'categoria'.")

    # Menú a insertar
platos = [
    (1,'Café Espresso','Un café intenso, preparado con granos recién molidos.',1500.00,'', 1),
    (2,'Café Capucchino','Un café intenso, preparado con granos recién molidos',1800.00,'', 1),
    (3,'Café Late','Un café intenso, preparado con granos recién molidos',2000.00,'', 1),
    (4,'Café Espresso','Un café intenso, preparado con granos recién molidos.',1500.00,'', 2),
    (5,'Café Capucchino','Un café intenso, preparado con granos recién molidos',1800.00,'', 2),
    (6,'Café Late','Un café intenso, preparado con granos recién molidos',2000.00,'', 2)  
    (7,'Torta Tres Leches','Torta con tres leches',4000.00,' static\torta3leches.png', 3)  
    (8,'Torta Chocolate','Torta rellena de chocolare',5000.00,'static\chocolate.png', 3)  
]

# Insertar los platos del Menú
cursor.executemany('''
    INSERT INTO menu (idmenu, nombremenu, descrimenu, preciomenu, idcategoria )
    VALUES (%s, %s,%s, %s,%s,%s)
''', platos)

print(f"Se han insertado {cursor.rowcount} registros en la tabla 'menu'.")

# Guardar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()






