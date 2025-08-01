from conectar import obtener_conexion
from flask import Flask, render_template,  request, redirect, flash, session, url_for, send_from_directory
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
# INICIAR SESION EN LA VISTA DEL MENU
#--------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def inicio():
    conn = obtener_conexion()
    if conn.is_connected():
        sql="SELECT * FROM `restaurante`.`empresa`"
        cursor = conn.cursor()
        cursor.execute(sql)
        db_empresa = cursor.fetchone()
        print(db_empresa)
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        # Valida el usuario y la contraseña
        if user == 'admin' and password == 'admin':  # Solo para prueba
            session['user'] = user
            return redirect(url_for('admin'))
    return render_template('/inicio.html', db_empresa=db_empresa,)

#--------------------------------------------------------------------
# SI EL USUARIO CONECTADO ES EL ADMIN MUESTRA EL MENU Y PERMITE EL CRUD
#--------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST']) 
def admin():
    if 'user' not in session:
        return redirect(url_for('inicio'))
    conn = obtener_conexion()
    if conn.is_connected(): 
        #print("Conexión exitosa a la base de datos.")
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
        #print("Sin Conexión a la base de datos.")
        return None  

#--------------------------------------------------------------------
#  MENU ADMINISTRADOR
#--------------------------------------------------------------------
@app.route('/menua') 
def indexAdmin():
    conn = obtener_conexion()
    if conn.is_connected(): 
        #print("Conexión exitosa a la base de datos.")
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
         #print("Sin Conexión a la base de datos.")
         return None

#--------------------------------------------------------------------
# FUNCION PARA EDITAR UN MENU
#--------------------------------------------------------------------
@app.route('/edit/<int:idmenu>')
def edit(idmenu):
    conn = obtener_conexion()
    if conn.is_connected():
       # print("Conexión exitosa a la base de datos.")
        cursor = conn.cursor()
        #Consulta el menú por id y agrega en la consulta el nombre de la categoria
        cursor.execute("SELECT m.*, c.nombrecat FROM restaurante.menu m, restaurante.categoria c WHERE m.idcategoria=c.idcategoria AND idmenu = %s", (idmenu,))
        menu = cursor.fetchone()
        #print(menu)
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
            _urlimgnew.save(f"static/images/{newNombreFoto}")
            

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
    try:
        # Obtener conexión y cursor
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Recibir datos del formulario
        _nombremenu  = request.form.get('txtnombremenu', '').strip()
        _descrimenu  = request.form.get('txtdescrimenu', '').strip()
        _preciomenu  = request.form.get('txtpreciomenu', '').strip()
        _idcategoria = request.form.get('txtidcategoria', '').strip()
        _urlimg = request.files.get('txturlimg')
        # Validar que los campos obligatorios no estén vacíos
        if not _nombremenu or not _descrimenu or not _preciomenu or not _idcategoria:
            flash("Por favor complete todos los campos obligatorios.")
            return redirect(url_for('admin'))
        # Procesar archivo
        filename = None
        if _urlimg and _urlimg.filename != '':
            filename = secure_filename(_urlimg.filename)
            # Asegurarse de que la carpeta exista
            upload_folder = os.path.join('static', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            # Guardar la imagen
            _urlimg.save(os.path.join(upload_folder, filename))
        # Preparar los datos para la inserción
        sql = """
            INSERT INTO `restaurante`.`menu` (idmenu, nombremenu, descrimenu, preciomenu, urlimg, idcategoria)
            VALUES (NULL, %s, %s, %s, %s, %s);
        """
        # Convertir precio a float, si es posible
        try:
            precio_float = float(_preciomenu)
        except ValueError:
            flash("El precio debe ser un número válido.")
            return redirect(url_for('admin'))
        datos = (_nombremenu, _descrimenu, precio_float, filename, _idcategoria)
        cursor.execute(sql, datos)
        conn.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        # Aquí puedes registrar el error para depuración
        print(f"Error en storage: {e}")
        flash("Ocurrió un error al guardar el menú.")
        return redirect(url_for('admin'))
    finally:
        # Cerrar conexión
        try:
            cursor.close()
            conn.close()
        except:
            pass
   

#--------------------------------------------------------------------
# FUNCION PARA CREAR LOS DATOS DE CONFIGURACION DE EMPRESA
#--------------------------------------------------------------------
@app.route('/configurar')
def configurar():
    # Obtener conexión y cursor
    conn = obtener_conexion()
    cursor = conn.cursor()
    #Consulta el menú por id y agrega en la consulta el nombre de la categoria
    cursor.execute("SELECT * FROM empresa")
    empresa = cursor.fetchone()
    print(empresa)
    return render_template('configurar.html', db_empresa = empresa,)

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
   #logo_filename = 'logoemp.png'
   # portada_filename = 'portadaemp.png'
    # Guardar logo si existe
    if _logoemp and _logoemp.filename != '':
        _logoemp.save(f"static/images/{_logoemp.filename}")   
    # Guardar portada si existe
    if _portadaemp and _portadaemp.filename != '':
        _portadaemp.save(f"static/images/{_portadaemp.filename}")
    # Construir la tupla de datos
    datos = (
        _rifemp,
        _nombremp,
        _descripemp,
        _direccemp,
        _horario,
        _logoemp,     # Guardamos el nombre fijo en la base
        _portadaemp,  # Guardamos el nombre fijo en la base
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
# FUNCION PARA EDITAR DATA DE EMPRESA
#--------------------------------------------------------------------
@app.route('/editconfig/<int:idempresa>')
def editconfig(idempresa):
    conn = obtener_conexion()
    if conn.is_connected():
        #print("Conexión exitosa a la base de datos.")
        cursor = conn.cursor()
        #Consulta el menú por id y agrega en la consulta el nombre de la categoria
        cursor.execute("SELECT * FROM restaurante.empresa WHERE idempresa=%s", (idempresa,))
        db_empresa = cursor.fetchone()
        cursor.close()
        return render_template('editconfig.html',  db_empresa=db_empresa, )
    
#--------------------------------------------------------------------
# FUNCION PARA MODIFICAR DATA DE EMPRESA
#--------------------------------------------------------------------    
@app.route('/updateconfig', methods=['POST'])
def updateconfig():
    _rifemp = request.form['txtrifemp']
    _nombremp = request.form['txtnombremp']
    _descripemp = request.form['txtdescripemp']
    _direccemp = request.form['txtdireccemp']
    _horario = request.form['txthorarioemp']
    _logoemp = request.files['txtlogoemp']
    _portadaemp= request.files['txtportadaemp']
    _mapa = request.form['txtmapa']
    _idempresa = request.form['txtidempresa']

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Actualizamos los datos básicos de Empresa
    sql = "UPDATE `restaurante`.`empresa` SET rifemp=%s, nombremp=%s, descripemp=%s, direccemp=%s, horario=%s, mapa=%s WHERE idempresa=%s"
    params = (_rifemp, _nombremp, _descripemp, _direccemp, _horario, _mapa, _idempresa)
    cursor.execute(sql, params)
     # Procesar la imagen
    if _logoemp and _logoemp.filename != '':
        # Guardar la imagen siempre con el nombre 'logoemp.png'
        filenamel = 'logoemp.png'
        ruta_destino = os.path.join(app.config['IMG_FOLDER'], filenamel)
        # Guardar la nueva imagen
        _logoemp.save(ruta_destino)
        # Si quieres eliminar la anterior, no es necesario porque siempre será la misma
        # pero si quieres asegurarte, puedes hacer esto:
        cursor.execute("SELECT logoemp FROM `restaurante`.`empresa` WHERE idempresa=%s", (_idempresa,))
        fila = cursor.fetchone()
        if fila and fila[0]:
            ruta_logo_antigua = os.path.join(app.config['IMG_FOLDER'], fila[0])
            if os.path.exists(ruta_logo_antigua) and fila[0] != filenamel:
                os.remove(ruta_logo_antigua) 
        if _portadaemp and _portadaemp.filename != '':
            filenamep = 'portadaemp.png'
            ruta_destino = os.path.join(app.config['IMG_FOLDER'], filenamep)
            # Guardar la nueva imagen
            _portadaemp.save(ruta_destino)
            # Si quieres eliminar la anterior, no es necesario porque siempre será la misma
            # pero si quieres asegurarte, puedes hacer esto:
            cursor.execute("SELECT portadaemp FROM `restaurante`.`empresa` WHERE idempresa=%s", (_idempresa,))
            fila = cursor.fetchone()
            if fila and fila[0]:
                ruta_port_antigua = os.path.join(app.config['IMG_FOLDER'], fila[0])
                if os.path.exists(ruta_port_antigua) and fila[0] != filenamep:
                    os.remove(ruta_port_antigua)            
            # Actualizar la base de datos con el nombre fijo
            cursor.execute("UPDATE `restaurante`.`empresa` SET portadaemp=%s  WHERE idempresa=%s", (filenamep,  _idempresa)) 
    conn.commit()
    cursor.execute("SELECT * FROM restaurante.empresa")
    db_empresa = cursor.fetchone()
    return render_template('configurar.html', db_empresa = db_empresa,)
#--------------------------------------------------------------------
# FUNCION PARA CERRAR SESION DE USUARIO
#--------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('inicio'))

#--------------------------------------------------------------------
# EJECUTAR APP
#--------------------------------------------------------------------
if __name__ == '__main__':
   app.run()
