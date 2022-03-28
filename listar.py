from flask import Flask, Response
import sqlite3
import json

database = 'database.db'
con = sqlite3.connect('database.db')
cur = con.cursor()
app = Flask(__name__)

def mapear_registros(atributos_tabla, cursor):
    registros = []
    
    for fila in cursor:
        registro = {}
        i = 0
        while i < len(fila):
            registro[atributos_tabla[i]] = fila[i]
            i += 1

        registros.append(registro)

    return registros


@app.route("/")
def index():
    atributos_arquitecto = [
        'arquitecto',
        'num_colegiado'
    ]

    atributos_edificio = [
        'id',
        'denominacion',
        'otrasDenominaciones',
        'categorias',
        'tipologia',
        'centro',
        'ubicacionActual',
        'acceso',
        'formaDeIngreso',
        'procedencia',
        'volumen',
        'cronologia',
        'autores',
        'descripcion',
        'historia',
        'objetoDocumento',
        'tecnicas',
        'signatura',
        'exposicion',
        'thumbnail'
    ]

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)

    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode([arquitectos, edificios]), mimetype='application/json')
