from flask import *
import json
import sqlite3

con = sqlite3.connect('database.db', check_same_thread=False)
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

@app.route('/buscar/<denominacion>')
def buscar(denominacion):
    '''Esta función permite realizar la búsqueda de un registro
    mediante el nombre del proyecto'''

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

    parametros = (denominacion,)
    sql = '''SELECT * FROM edificio WHERE denominacion LIKE '%?%' '''
    
    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_edificio, cur)
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')
