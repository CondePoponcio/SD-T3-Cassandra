from flask import Flask, jsonify, request
from flask_json_schema import JsonSchema, JsonValidationError
from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory, dict_factory
import os

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import traceback
import json
from operator import itemgetter
import uuid

app = Flask(__name__)
schema = JsonSchema(app)

def connectDatabase():
    return psycopg2.connect(
        host="database",
        database="tiendita",
        user='postgres',
        password='marihuana'
    )

def connectCassandra(keyspace):
    cluster = Cluster(contact_points=[ os.environ["CASSANDRA_IP_ADDRESS"] ], port=9042)
    session = cluster.connect(keyspace)
    return session

def queryDatabase(nombre): 
        
    largo=len(nombre)

    conn = connectDatabase()

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM items WHERE name LIKE '%"+nombre+"%'")
    
    row = cur.fetchall()

    val = json.dumps(row)

    conn.commit()

    cur.close()
    conn.close()

    return row




@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400

def printLogs(ex_type, ex_value, ex_traceback):
    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)
    # Format stacktrace
    stack_trace = ["File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]) for trace in trace_back ]
    print("Exception type : %s" % ex_type.__name__)
    print("Exception message : %s" %ex_value)
    print("Stack trace : %s" %stack_trace)

@app.route('/delete', methods=['POST'])
@schema.validate({
    'required': ['id'],
    'properties': {
        'id': { 'type': 'string' },
    }
})
def delete():
    
    try:
        payload = request.get_json()
        id = itemgetter('id')(payload)

        session = connectCassandra('recetas_ks')
        session.execute(""" 
            DELETE FROM recetas WHERE id = %s
        """, [uuid.UUID(id)])
        
        return jsonify({"status: ": 'success'}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception type : %s " % ex_type.__name__}), 500


@app.route('/edit', methods=['POST'])
@schema.validate({
    'required': ['id', 'comentario', 'farmacos', 'doctor'],
    'properties': {
        'comentario': { 'type': 'string' },
        'farmacos': { 'type': 'string' },
        'doctor': { 'type': 'string' },
        'id': { 'type': 'string' },
    }
})
def edit():
    
    try:
        payload = request.get_json()
        id, comment, farmacos, doc = itemgetter('id','comentario',
        'farmacos',
        'doctor')(payload)

        session = connectCassandra('recetas_ks')
        session.execute(""" 
            UPDATE recetas SET comentario = %s, farmacos = %s, doctor = %s WHERE id = %s IF EXISTS
        """, [comment, farmacos, doc, uuid.UUID(id)])
        
        return jsonify({"status: ": 'success'}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception type : %s " % ex_type.__name__}), 500


@app.route('/create', methods=['POST'])
@schema.validate({
    'required': ['nombre', 'apellido', 'rut', 'email', 'fecha_nacimiento', 'comentario', 'farmacos', 'doctor'],
    'properties': {
        'nombre': { 'type': 'string' },
        'apellido': { 'type': 'string' },
        'rut': { 'type': 'string' },
        'email': { 'type': 'string' },
        'fecha_nacimiento': { 'type': 'string' },
        'comentario': { 'type': 'string' },
        'farmacos': { 'type': 'string' },
        'doctor': { 'type': 'string' },
        'priority': { 'type': 'integer' },
    }
})
def create():
    
    try:
        session = connectCassandra('paciente_ks')
        payload = request.get_json()
        nombre, apellido, rut, email, fecha, comment, farmacos, doc = itemgetter('nombre', 
        'apellido',
        'rut',
        'email',
        'fecha_nacimiento',
        'comentario',
        'farmacos',
        'doctor')(payload)

        session.row_factory = dict_factory
        users = session.execute("select * from paciente where nombre = %s", [nombre])
        
        response = []
        for user in list(users):
            temp = dict(user)
            temp["id"] = str(user["id"])
            response.append(temp)
        
        if len(response) == 0:
            newUserId = uuid.uuid4()
            insertresponse = session.execute(""" 
                INSERT INTO paciente (id, nombre, apellido, rut, email, fecha_nacimiento)
                values (%s, %s, %s, %s, %s, %s)
            """, [newUserId, nombre, apellido, rut, email, fecha])
            newUserId = str( newUserId )
        else: 
            newUserId = response[0]["id"]
        
        session = connectCassandra('recetas_ks')
        newRecetaId = uuid.uuid4()
        session.execute(""" 
            INSERT INTO recetas (id, id_paciente, comentario, farmacos, doctor)
            values (%s, %s, %s, %s, %s)
        """, [newRecetaId, uuid.UUID(newUserId), comment, farmacos, doc])
        
        return jsonify({"status: ": 'success'}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception type : %s %s" % (ex_type.__name__, ex_value)}), 500
    
@app.route('/all', methods=['POST'])
def getAll():
    
    try:
        session = connectCassandra('paciente_ks')
        
        session.row_factory = dict_factory
        users = session.execute("select * from paciente")
        
        users_response = []
        for user in list(users):
            temp = dict(user)
            temp["id"] = str(user["id"])
            users_response.append(temp)
        
        session = connectCassandra('recetas_ks')
        
        session.row_factory = dict_factory
        recetas = session.execute("select * from recetas")
        
        recetas_response = []
        for item in list(recetas):
            temp = dict(item)
            temp["id"] = str(item["id"])
            temp["id_paciente"] = str(item["id_paciente"])
            recetas_response.append(temp)
        
        return jsonify({"pacientes: ": users_response, "recetas": recetas_response}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception type : %s %s" % (ex_type.__name__, ex_value)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)