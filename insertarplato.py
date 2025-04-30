from conectar import obtener_conexion

# Obtener la conexión
conn = obtener_conexion()
cursor = conn.cursor()


# Menú a insertar
platos = [
    (1,'Café Espresso','Un café intenso, preparado con granos recién molidos.',1500.00, 1),
    (2,'Café Capucchino','Un café intenso, preparado con granos recién molidos',1800.00, 1),
    (3,'Café Late','Un café intenso, preparado con granos recién molidos',2000.00, 1),
    (4,'Café Espresso','Un café intenso, preparado con granos recién molidos.',1500.00, 2),
    (5,'Café Capucchino','Un café intenso, preparado con granos recién molidos',1800.00, 2),
    (6,'Café Late','Un café intenso, preparado con granos recién molidos',2000.00, 2)  
]

# Insertar los platos del Menú
cursor.executemany('''
    INSERT INTO menu (idmenu, nombremenu, descrimenu, preciomenu, idcategoria )
    VALUES (%s, %s,%s, %s,%s)
''', platos)

print(f"Se han insertado {cursor.rowcount} registros en la tabla 'menu'.")

# Guardar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()









