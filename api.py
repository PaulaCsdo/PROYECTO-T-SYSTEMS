from flask import *
import sqlite3
import json

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


@app.route("/")
def index():
    atributos_arquitecto = [
        'arquitecto',
        'num_colegio'
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


@app.route("/Edificio/eliminar/<id>")
def eliminar_edificio(id):
    
    parametros = (id,)
    sql = "DELETE FROM edificio WHERE id = ?;"
    
    try:
        cur.execute(sql, parametros)
        con.commit()
    except:
        return 'No se ha podido eliminar el registro'

    return redirect(url_for('index'))


@app.route("/Arquitecto/eliminar/<arquitecto>")
def eliminar_arquitecto(arquitecto):

    parametros = (arquitecto,)
    sql = "DELETE FROM arquitecto WHERE arquitecto = '?';"

    try:
        cur.execute(sql, parametros)
        con.commit()
    except:
        return 'No se ha podido eliminar el registro'

    return redirect(url_for('index'))


app.route('/buscar/<denominacion>')
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
