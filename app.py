from conectar import obtener_conexion
from flask import Flask, render_template,  request,redirect, session,url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__) 
app.secret_key = '1234'

#--------------------------------------------------------------------
# SE ESTABLECE  CARPETA DE IMAGENES
#--------------------------------------------------------------------
app.config['STATIC_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
app.config['IMG_FOLDER'] = os.path.join(app.config['STATIC_FOLDER'], 'images')

#--------------------------------------------------------------------
# GUARDAMOS LA RUTA DE LA CARPETA uploads EN LA APP
#--------------------------------------------------------------------
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#--------------------------------------------------------------------
# Generamos el acceso a la carpeta fotos. 
# El método fotos que creamos nos dirige a la carpeta (variable CARPETA)
# y nos muestra la foto guardada en la variable fotomenu.
#--------------------------------------------------------------------
@app.route('/uploads/<fotomenu>')
def uploads(fotomenu):
 return send_from_directory(app.config['CARPETA'], fotomenu)

#--------------------------------------------------------------------
# INICIAR SESION EN LA VISTA DEL MENU
#--------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        # Valida el usuario y la contraseña
        if user == 'admin' and password == 'admin':  # Solo para prueba
            session['user'] = user
            return redirect(url_for('admin'))
    return render_template('/inicio.html')

#--------------------------------------------------------------------
# SI EL USUARIO CONECTADO ES EL ADMIN MUESTRA EL MENU Y PERMITE EL CRUD
#--------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST']) 
def admin():
    if 'user' not in session:
        return redirect(url_for('inicio'))
    conn = obtener_conexion()
    if conn.is_connected(): 
        print("Conexión exitosa a la base de datos.")
        # Consulta cada plato del menú con su categoria
        sql = "SELECT a.*, r.idcategoria, r.nombrecat FROM menu a JOIN categoria r ON a.idcategoria = r.idcategoria;"
        cursor = conn.cursor()
        cursor.execute(sql)
        db_menu = cursor.fetchall()
        #Consulta las categorias
        sql = "SELECT * FROM categoria;"
        cursor.execute(sql)
        db_categoria = cursor.fetchall()      
        #Consulta datos de Empresa
        sql = "SELECT * FROM restaurante.empresa;"
        cursor.execute(sql)
        db_empresa = cursor.fetchone()   
        # Devolvemos código HTML para ser renderizado
        return render_template('tablarest.html', menu=db_menu, categoria=db_categoria, db_empresa=db_empresa, )
    else:
        print("Sin Conexión a la base de datos.")
        return None  

#--------------------------------------------------------------------
#  MENU ADMINISTRADOR
#--------------------------------------------------------------------
@app.route('/menua') 
def indexAdmin():
    conn = obtener_conexion()
    if conn.is_connected(): 
        print("Conexión exitosa a la base de datos.")
        # Consulta cada plato del menú con su categoria
        sql = "SELECT a.*, r.nombrecat FROM menu a JOIN categoria r ON a.idcategoria = r.idcategoria;"
        cursor = conn.cursor()
        cursor.execute(sql)
        db_menu = cursor.fetchall()    
        #Consulta las categorias
        sql = "SELECT * FROM categoria;"
        cursor.execute(sql)
        db_categoria = cursor.fetchall()
        sql = "SELECT * FROM empresa;"
        cursor.execute(sql)
        db_empresa = cursor.fetchone()
        #Devolvemos código HTML para ser renderizado
        return render_template('indexAdmin.html', menu=db_menu, categoria=db_categoria, db_empresa=db_empresa,)
    else:
         print("Sin Conexión a la base de datos.")
         return None

#--------------------------------------------------------------------
#  MENU CLIENTE
#--------------------------------------------------------------------
@app.route('/menuc') 
def cliente():
    conn = obtener_conexion()
    if conn.is_connected(): 
        print("Conexión exitosa a la base de datos.")
        # Consulta cada plato del menú con su categoria
        sql = "SELECT a.*, r.nombrecat FROM menu a JOIN categoria r ON a.idcategoria = r.idcategoria;"
        cursor = conn.cursor()
        cursor.execute(sql)
        db_menu = cursor.fetchall()    
        #Consulta las categorias
        sql = "SELECT * FROM categoria;"
        cursor.execute(sql)
        db_categoria = cursor.fetchall()
        #Devolvemos código HTML para ser renderizado
        return render_template('index.html', menu=db_menu, categoria=db_categoria,)
    else:
         print("Sin Conexión a la base de datos.")
         return None

#--------------------------------------------------------------------
# FUNCION PARA EDITAR UN MENU
#--------------------------------------------------------------------
@app.route('/edit/<int:idmenu>')
def edit(idmenu):
    conn = obtener_conexion()
    if conn.is_connected():
        print("Conexión exitosa a la base de datos.")
        cursor = conn.cursor()
        #Consulta el menú por id y agrega en la consulta el nombre de la categoria
        cursor.execute("SELECT m.*, c.nombrecat FROM restaurante.menu m, restaurante.categoria c WHERE m.idcategoria=c.idcategoria AND idmenu = %s", (idmenu,))
        menu = cursor.fetchone()
        print(menu)
        conn.commit()
        sql = "select * FROM restaurante.empresa" 
        cursor.execute(sql)
        db_empresa = cursor.fetchone()
        conn.commit()
        sql = "SELECT * FROM categoria;"
        cursor.execute(sql)
        categoria = cursor.fetchall() 
        return render_template('edit.html', menu = menu , db_empresa=db_empresa,  categoria = categoria,)
    
#--------------------------------------------------------------------
# FUNCION PARA MODIFICAR UN MENU DEL CATALOGO
#--------------------------------------------------------------------
@app.route('/update', methods=['POST'])
def update():
    _nombremenu    = request.form['txtnombremenu']
    _descrimenu    = request.form['txtdescrimenu']
    _preciomenu    = request.form['txtpreciomenu']
    _urlimgnew    = request.files.get('txturlimgnew')
    _idcategorianew = request.form['txtidcategorianew']
    _idmenu        = request.form['txtidmenu']
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Obtener categoria actual del menu antes de la actualización
    cursor.execute("SELECT idcategoria, urlimg FROM restaurante.menu WHERE idmenu=%s", (_idmenu,))
    fila_actual = cursor.fetchone()
    categ_actual = fila_actual[0] if fila_actual else None
    urlimg_actual = fila_actual[1] if fila_actual else None

    if conn.is_connected():
        # Verificar si la categoría ha cambiado
        if categ_actual != _idcategorianew:
            params = (_nombremenu, _descrimenu, _preciomenu, _idcategorianew, _idmenu)
        else:
            params = (_nombremenu, _descrimenu, _preciomenu, categ_actual, _idmenu)
            # Preparar la consulta de actualización
        sql = "UPDATE restaurante.menu SET nombremenu=%s, descrimenu=%s, preciomenu=%s, idcategoria=%s WHERE idmenu=%s"
        cursor.execute(sql, params)

        # Si se subió una nueva imagen
        if _urlimgnew and _urlimgnew.filename != '':
            # Guardar la nueva imagen
            newNombreFoto = secure_filename(_urlimgnew.filename)
            ruta_guardar = os.path.join(app.config['CARPETA'], newNombreFoto)
            _urlimgnew.save(ruta_guardar)

            # Borrar la foto anterior si existe
            if urlimg_actual:
                rutaFotoAnterior = os.path.join(app.config['CARPETA'], urlimg_actual)
                if os.path.exists(rutaFotoAnterior):
                    os.remove(rutaFotoAnterior)

            # Actualizar la base de datos con el nuevo nombre de la foto
            cursor.execute("UPDATE restaurante.menu SET urlimg=%s WHERE idmenu=%s", (newNombreFoto, _idmenu))
        conn.commit()
        cursor.close()
    return redirect(url_for('admin'))

#--------------------------------------------------------------------
# FUNCION PARA ELIMINAR UN MENU DEL CATALOGO
#--------------------------------------------------------------------
@app.route('/destroy/<int:idmenu>')
def destroy(idmenu):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE idmenu=%s", (idmenu,))
    conn.commit()
    cursor.close()
    return redirect(url_for('admin'))

#--------------------------------------------------------------------
# FUNCION PARA CREAR UN MENU EN EL CATALOGO
#--------------------------------------------------------------------
@app.route('/create')
def create():
    conn = obtener_conexion()
    cursor = conn.cursor()
    sql="SELECT * FROM restaurante.empresa"
    cursor.execute(sql) 
    db_empresa=cursor.fetchone()
    conn.commit()  
    sql="SELECT * FROM restaurante.categoria"
    cursor.execute(sql) 
    categoria=cursor.fetchall()
    cursor.close()
    return render_template('create.html', db_empresa = db_empresa, categoria = categoria,)

#--------------------------------------------------------------------
# FUNCION PARA ALMACENAR UN MENU EN EL CATALOGO
#--------------------------------------------------------------------
@app.route('/store', methods=['POST'])
def storage():
    # Obtener conexión y cursor
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Recibir datos del formulario
    _nombremenu  = request.form['txtnombremenu']
    _descrimenu  = request.form['txtdescrimenu']
    _preciomenu  = request.form['txtpreciomenu']
    _idcategoria = request.form['txtidcategoria']
    # Procesar archivo
    _urlimg = request.files.get('txturlimg')

    # Variable para guardar el nombre del archivo
    filename = None

    if _urlimg and _urlimg.filename != '':
        # Puedes asegurar que el nombre del archivo sea seguro
        filename = secure_filename(_urlimg.filename)
        # Guardar la imagen en la carpeta deseada
        _urlimg.save(f"static/images/{filename}")

    # Preparar los datos para la inserción
    sql = """
        INSERT INTO restaurante.menu (idmenu, nombremenu, descrimenu, preciomenu, urlimg, idcategoria)
        VALUES (NULL, %s, %s, %s, %s, %s);
    """
    # La variable filename puede ser None si no se cargó imagen
    datos = (_nombremenu, _descrimenu, _preciomenu, filename, _idcategoria)
    cursor.execute(sql, datos)
    conn.commit()
    return redirect(url_for('admin'))

#--------------------------------------------------------------------
# FUNCION PARA CREAR LOS DATOS DE CONFIGURACION DE EMPRESA
#--------------------------------------------------------------------
@app.route('/configurar')
def configurar():
    return render_template('configurar.html')

#--------------------------------------------------------------------
# FUNCION PARA ALMACENAR LOS DATOS DE CONFIGURACION DE EMPRESA
#--------------------------------------------------------------------
@app.route('/storeconfig', methods=['POST'])
def storageconfig():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    conn = obtener_conexion()
    cursor = conn.cursor()
    _rifemp  = request.form['txtrifemp']
    _nombremp  = request.form['txtnombremp']
    _descripemp  = request.form['txtdescripemp']
    _direccemp  = request.form['txtdireccemp']
    _horario      = request.form['txthorarioemp']
    _mapa = request.form['txtmapa']  
    # Procesar archivos
    _logoemp = request.files.get('txtlogoemp')
    _portadaemp = request.files.get('txtportadaemp') 
    # Definir nombres fijos para las imágenes
    logo_filename = 'logoemp.png'
    portada_filename = 'portadaemp.png'
    # Guardar logo si existe
    if _logoemp and _logoemp.filename != '':
        _logoemp.save(f"static/images/{logo_filename}")   
    # Guardar portada si existe
    if _portadaemp and _portadaemp.filename != '':
        _portadaemp.save(f"static/images/{portada_filename}")
    # Construir la tupla de datos
    datos = (
        _rifemp,
        _nombremp,
        _descripemp,
        _direccemp,
        _horario,
        logo_filename,     # Guardamos el nombre fijo en la base
        portada_filename,  # Guardamos el nombre fijo en la base
        _mapa
    )
    # Ejecutar la consulta
    sql = """
        INSERT INTO restaurante.empresa
        (idempresa, rifemp, nombremp, descripemp, direccemp, horario, logoemp, portadaemp, mapa)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(sql, datos)
    conn.commit()
    return redirect(url_for('admin'))

#--------------------------------------------------------------------
# FUNCION PARA CERRAR SESION DE USUARIO
#--------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('inicio'))

    
if __name__ == '__main__':
        app.run(debug=True)