from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS  # Importa CORS

import datetime

app = Flask(__name__)
CORS(app)
# Configuración de MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'estadisticas'

orm = MySQL(app)

@app.route('/jugadores',methods=['GET'])
def getJugadores():
    conn = orm.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jugador")
    data = cursor.fetchall()
    return str(data)

@app.route('/jugadores/crearJugador',methods=['POST'])
def saveJugador():
    content = request.json
    conn = orm.connect()
    cursor = conn.cursor()
    query = """INSERT INTO jugador (`id_jugador`,`usuario`,`nombre`,`apellido`,`mail`) VALUES (%s,%s,%s,%s,%s)"""
    print(query, tuple(content.values()))
    try:
     cursor.execute(query, tuple(content.values()))
     conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"Ok":"Jugador guardado"}),201
if __name__ == '__main__':
    app.run(debug=True)