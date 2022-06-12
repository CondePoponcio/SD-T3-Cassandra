from flask import Flask, jsonify, request
from flask_json_schema import JsonSchema, JsonValidationError

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import traceback
import json
from operator import itemgetter

app = Flask(__name__)
schema = JsonSchema(app)

def connectDatabase():
    return psycopg2.connect(
        host="database",
        database="tiendita",
        user='postgres',
        password='marihuana'
    )

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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    if not data.get('user') or not data.get('pass'):
        return jsonify({'error': 'Missing data'}), 400
    user = User.query.filter_by(user=data['user']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    response = requests.get("http://flask-api-blocked:5000/blocked")
    
    response = response.json()
    banned_users = response["users-blocked"]
    
    if data['user'] in banned_users:
        return jsonify({'error': 'User Banned'}), 400    
    if not bcrypt.checkpw(data['pass'].encode('utf-8'), user.password.encode('utf-8')):
        asyncio.run(send_one(data['user']))
        return jsonify({'error': 'Wrong password'}), 401
    
    return jsonify({'success': True}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("data:", data)
    answer = register_check(data)
    return answer
@app.route('/usuarios', methods=['GET','DELETE'])
def get_body():
    if request.method == 'GET':
        if request.args.get('id'):
            user = User.query.filter_by(id=request.args.get('id')).first()
            if user:
                return jsonify(to_dict(user))
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            users = User.query.all()
            return jsonify([to_dict(user) for user in users])
    elif request.method == 'DELETE':
        if request.args.get('id'):
            user = User.query.filter_by(id=request.args.get('id')).first()
            if user:
                user_name = user.name
                db.session.delete(user)
                db.session.commit()
                return jsonify({"message": "User "+user_name+" deleted"}), 200
            else:
                return jsonify({"error": "User not found"}), 404


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
    payload = request.get_json(silent=True)
    if payload:
        """
        pluck = lambda dict, *args: (dict[arg] for arg in args)

        things = {'blah': 'bleh', 'foo': 'bar'}
        foo, blah = pluck(things, 'foo', 'blah', "boy")
        """

        try:
            key_1, key_2 = itemgetter('nombre', 
            'apellido',
            'rut',
            'email',
            'fecha_nacimiento',
            'comentario',
            'farmacos',
            'doctor')(payload)

            print(key_1, key_2)
            return jsonify([key_1, key_2])
        except Exception as e:
            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            print("Error: ", type(ex_value))
            return jsonify({"error": "Exception type : %s " % ex_type.__name__}), 400
    else:
        return jsonify({"error": "No hay datos enviados"}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)