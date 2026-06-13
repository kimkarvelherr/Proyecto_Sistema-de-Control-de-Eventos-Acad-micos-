from flask import Flask, jsonify, render_template, request
import pymysql
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
app = Flask(__name__)

# Clave secreta para JWT
app.config['JWT_SECRET_KEY'] = '123'
jwt = JWTManager(app)


#conexion a la BD tienda_db en mysql
def getConexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="eventos_academicos"
    )

#####RENDER TEMPLATE #######
@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/evento_html')
def evento_html():
    return render_template('evento.html')

@app.route('/participante_html')
def participante_html():
    return render_template('participante.html')

@app.route('/inscripcion_html')
def inscripcion_html():
    return render_template('inscripcion.html')

@app.route('/asistencia_html')
def asistencia_html():
    return render_template('asistencia.html')



@app.route('/testdb')
def test():
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    cursor.close()
    conexion.close()
    return "conexion exitosa!!!"

#------------------------------
# LOGIN
#------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == '123':
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    return jsonify({"error": "credenciales incorrectas"}), 401

#------------------------------
# ENDPOINTS GET 
#------------------------------
###############    GET ASISTENCIA   ###############
@app.route('/asistencia', methods=['GET'])
def listar_asistencia():
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = """SELECT id_asistencia, id_participante, 
             id_evento,fecha_registro, asistio 
             FROM asistencia"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if not datos:
        msg = {
            "mensage": "No existen asistencias!!"
        }
        return jsonify(msg)
   
    asistencia = []
    for fila in datos:
        asistencia.append(
            {
                "id_asistencia": fila[0],
                "id_participante": fila[1],
                "id_evento": fila[2],
                "fecha_registro": fila[3],
                "asistio": fila[4]
            }
        )
    cursor.close()
    conexion.close()
    return jsonify(asistencia)




###############    GET EVENTO  ###############
@app.route('/evento', methods=['GET'])
def listar_evento():
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = """SELECT id_evento, nombre, descripcion,
             fecha, hora,lugar, tipo_evento, capacidad 
             FROM evento"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if not datos:
        msg = {
            "mensage": "No existen eventos!!"
        }
        return jsonify(msg)
   
    evento = []
    for fila in datos:
        evento.append(
            {
                "id_evento": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "fecha": str(fila[3]),
                "hora": str(fila[4]),
                "lugar": fila[5],
                "tipo_evento": fila[6],
                "capacidad": fila[7]
            }
        )
    cursor.close()
    conexion.close()
    return jsonify(evento)

###############    GET INSCRIPCION   ###############
@app.route('/inscripcion', methods=['GET'])
def listar_inscripcion():
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = """SELECT id_inscripcion, id_participante, 
             id_evento,fecha_inscripcion, estado 
             FROM inscripcion"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if not datos:
        msg = {
            "mensage": "No existen inscripciones!!"
        }
        return jsonify(msg)
   
    inscripcion = []
    for fila in datos:
        inscripcion.append(
            {
                "id_inscripcion": fila[0],
                "id_participante": fila[1],
                "id_evento": fila[2],
                "fecha_inscripcion": fila[3],
                "estado": fila[4]
            }
        )
    cursor.close()
    conexion.close()
    return jsonify(inscripcion)


###############    GET PARTICIPANTE   ###############
@app.route('/participante', methods=['GET'])
def listar_participantes():
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "SELECT id_participante, nombres, apellidos,correo, telefono, institucion FROM participante"
    cursor.execute(sql)
    datos = cursor.fetchall()

    if not datos:
        msg = {
            "mensage": "No existen participantes!!"
        }
        return jsonify(msg)
   
    participantes = []
    for fila in datos:
        participantes.append(
            {
                "id_participante": fila[0],
                "nombres": fila[1],
                "apellidos": fila[2],
                "correo": fila[3],
                "telefono": fila[4],
                "institucion": fila[5]
            }
        )
    cursor.close()
    conexion.close()
    return jsonify(participantes)

#------------------------------
# ENDPOINTS POST
#------------------------------
#### POST ASISTENCIA ######
@app.route('/asistencia', methods=['POST'])
@jwt_required()
def insertar_asistencia():
    #recuperar datos en formato json
    data = request.get_json()
    id_participante = data.get("id_participante")
    id_evento=data.get("id_evento")
    fecha_registro=data.get("fecha_registro")
    asistio=data.get("asistio")
    
    #insertar la tabla aistencia
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO asistencia(id_participante,id_evento,fecha_registro,asistio) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (id_participante,id_evento,fecha_registro,asistio,))
    conexion.commit() 
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Asistencia registrada con éxito!"}), 201


#### POST EVENTO ######
@app.route('/evento', methods=['POST'])
@jwt_required()
def insertar_evento():
    #recuperar datos en formato json
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion=data.get("descripcion")
    fecha=data.get("fecha")
    hora=data.get("hora")
    lugar=data.get("lugar")
    tipo_evento=data.get("tipo_evento")
    capacidad=data.get("capacidad")
    
    #insertar la tabla evento
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO evento(nombre,descripcion,fecha,hora,lugar,tipo_evento,capacidad) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (nombre,descripcion,fecha,hora,lugar,tipo_evento,capacidad,))
    conexion.commit() 
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Evento registrada con éxito!"}), 201


#### POST INSCRIPCION ######
@app.route('/inscripcion', methods=['POST'])
@jwt_required()
def insertar_inscripcion():
    #recuperar datos en formato json
    data = request.get_json()
    id_participante = data.get("id_participante")
    id_evento = data.get("id_evento")
    fecha_inscripcion = data.get("fecha_inscripcion")
    estado = data.get("estado")
    
    
    #insertar la tabla inscripcion
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO inscripcion(id_participante,id_evento,fecha_inscripcion,estado) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (id_participante,id_evento,fecha_inscripcion,estado,))
    conexion.commit() 
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Evento registrada con éxito!"}), 201


#### POST PARTICIPANTE ######
@app.route('/participante', methods=['POST'])
@jwt_required()
def insertar_participante():
    #recuperar datos en formato json
    data = request.get_json()
    nombres = data.get("nombres")
    apellidos=data.get("apellidos")
    correo=data.get("correo")
    telefono=data.get("telefono")
    institucion=data.get("institucion")
    
    #insertar la tabla participante
    conexion = getConexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO participante(nombres,apellidos,correo,telefono,institucion) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (nombres,apellidos,correo,telefono,institucion,))
    conexion.commit() 
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Participante registrada con éxito!"}), 201



if __name__ == "__main__":
    app.run(debug=True)
