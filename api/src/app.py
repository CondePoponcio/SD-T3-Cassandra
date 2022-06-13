import os
import sys
import traceback
import json
import uuid

from flask import Flask, jsonify, request
from flask_json_schema import JsonSchema, JsonValidationError

from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory, dict_factory

from operator import itemgetter
from marshmallow import Schema, fields, post_load

from utils.ErrorMessage import printLogs
from utils.model.receta import Receta, RecetaSchema
from utils.model.paciente import Paciente, PacienteSchema


app = Flask(__name__)
schema = JsonSchema(app)

def connectCassandra(keyspace):
    cluster = Cluster(contact_points=[ os.environ["CASSANDRA_IP_ADDRESS"] ], port=9042)
    session = cluster.connect(keyspace)
    return session


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400


@app.route('/delete', methods=['POST'])
def delete():
    try:
        payload = request.get_json()
        
        receta = RecetaSchema().load(payload, partial=('comentario', 'doctor', 'farmacos', 'id_paciente'), unknown='exclude')
        
        id = itemgetter('id')(receta) 

        session = connectCassandra('recetas_ks')
        session.execute("DELETE FROM recetas WHERE id = %s", [id])
        
        return jsonify({"status: ": 'success'}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception message : %s " % ex_value}), 400


@app.route('/edit', methods=['POST'])
def edit():
    
    try:
        payload = request.get_json()
        receta = RecetaSchema().load(payload, partial=('id_paciente',), unknown='exclude')
        
        id, comment, farmacos, doc = itemgetter('id','comentario',
        'farmacos',
        'doctor')(receta)

        session = connectCassandra('recetas_ks')
        session.execute(""" 
            UPDATE recetas SET comentario = %s, farmacos = %s, doctor = %s WHERE id = %s IF EXISTS
        """, [comment, farmacos, doc, id])
        
        return jsonify({"status: ": 'success'}) 
    except Exception as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printLogs(ex_type, ex_value, ex_traceback)
        return jsonify({"error": "Exception message : %s " % ex_value}), 400


@app.route('/create', methods=['POST'])
def create():
    
    try:
        session = connectCassandra('paciente_ks')
        
        payload = request.get_json()
        receta = RecetaSchema().load(payload, partial=('id', 'id_paciente'), unknown='exclude')
        paciente = PacienteSchema().load(payload, partial=('id'), unknown='exclude')
        
        payload = {**receta, **paciente}
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

            session.row_factory = dict_factory
            insertresponse = session.execute(""" 
                INSERT INTO paciente (id, nombre, apellido, rut, email, fecha_nacimiento)
                values (%s, %s, %s, %s, %s, %s)
            """, [newUserId, nombre, apellido, rut, email, fecha], trace=True)
            
        else: 
            newUserId = uuid.UUID(response[0]["id"])
        
        session = connectCassandra('recetas_ks')
        newRecetaId = uuid.uuid4()
        session.execute(""" 
            INSERT INTO recetas (id, id_paciente, comentario, farmacos, doctor)
            values (%s, %s, %s, %s, %s)
        """, [newRecetaId, newUserId, comment, farmacos, doc])
        
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