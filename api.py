from flask import *
import sqlite3
import json

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()
app = Flask(__name__)


def devolver_atrib_arquitecto():
    return [
        'arquitecto',
        'num_colegio'
    ]


def devolver_atrib_edificio():
    return [
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

    atributos_arquitecto = devolver_atrib_arquitecto()
    atributos_edificio = devolver_atrib_edificio()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)

    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode([arquitectos, edificios]), mimetype='application/json')


@app.route("/Edificio")
def index_edificio():
    atributos_edificio = devolver_atrib_edificio()
    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode(edificios), mimetype='application/json')


@app.route("/Arquitecto")
def index_arquitecto():
    atributos_arquitecto = devolver_atrib_arquitecto()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)
    
    return Response(json.JSONEncoder().encode(arquitectos), mimetype='application/json')


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
    sql = "DELETE FROM arquitecto WHERE arquitecto = ?;"

    try:
        cur.execute(sql, parametros)
        con.commit()
    except:
        return 'No se ha podido eliminar el registro'

    return redirect(url_for('index'))


@app.route('/Edificio/buscar/<denominacion>')
def buscar_edificio(denominacion):
    '''Esta función permite realizar la búsqueda de un registro
    mediante el nombre del proyecto'''

    atributos_edificio = devolver_atrib_edificio()
    
    try:
        cur.execute('''SELECT * FROM edificio WHERE denominacion LIKE '%{}%' '''.format(denominacion))
    except:
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_edificio, cur)
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')


@app.route('/Arquitecto/buscar/<arquitecto>')
def buscar_arquitecto(arquitecto):
    '''Esta función permite realizar la búsqueda de un registro
    mediante el nombre del proyecto'''

    atributos_arquitecto = devolver_atrib_arquitecto()
    
    try:
        cur.execute('''SELECT * FROM arquitecto WHERE arquitecto LIKE '%{}%' '''.format(arquitecto))
    except:
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_arquitecto, cur)
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')


@app.route('/Edificio/modificar', methods=['GET', 'POST'])
def modificar_edificio():
    con = sqlite3.connect('database.db', check_same_thread=False)
    
    if request.method == 'GET':
        atributos_edificio = devolver_atrib_edificio()
        try:
            cur.execute('''SELECT * FROM edificio WHERE id={}'''.format(request.args.get('id')))
        except:
            return 'No se ha podido realizar la búsqueda'

        busqueda = mapear_registros(atributos_edificio, cur)
        con.commit()

        return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')

    elif request.method == 'POST':
        data = json.loads(request.data)

        for atributo, nuevo_valor in data.items():
            parametros = (nuevo_valor, data['id'])
            sql = '''UPDATE edificio set {} = ? WHERE id = ?'''.format(atributo)
            try:
                cur.execute(sql, parametros)
            except:
                return 'No se ha podido actualizar el registro'
            
        con.commit()
        
        return redirect(url_for('index'))    


@app.route('/Arquitecto/modificar', methods=['GET', 'POST'])
def modificar_arquitecto():
    con = sqlite3.connect('database.db', check_same_thread=False)
    
    if request.method == 'GET':
        atributos_arquitecto = devolver_atrib_arquitecto()
        try:
            cur.execute('''SELECT * FROM arquitecto WHERE arquitecto={}'''.format(request.args.get('arquitecto')))
        except:
            return 'No se ha podido realizar la búsqueda'

        busqueda = mapear_registros(atributos_arquitecto, cur)
        con.commit()

        return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')

    elif request.method == 'POST':
        data = json.loads(request.data)

        for atributo, nuevo_valor in data.items():
            parametros = (nuevo_valor, data['arquitecto'])
            sql = '''UPDATE arquitecto set {} = ? WHERE arquitecto = ?'''.format(atributo)
            try:
                cur.execute(sql, parametros)
            except:
                return 'No se ha podido actualizar el registro'
            
        con.commit()
        
        return redirect(url_for('index'))

@app.route('/Arquitecto/anadir', methods=['POST'])
def anadir_arquitecto():
    data = json.loads(request.data)
    atributos_arquitecto = devolver_atrib_arquitecto()
    
    parametros = (data['arquitecto'], data['num_colegio'])
    sql = """ INSERT INTO arquitecto (arquitecto, num_colegio) 
                          VALUES (?, ?) """

    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido insertar el registro'
            
    con.commit()
        
    return redirect(url_for('index'))

        
@app.route('/Edificio/anadir', methods=['POST'])
def anadir_edificio():
    data = json.loads(request.data)
    atributos_edificio = devolver_atrib_edificio()
    
    parametros = tuple([str(valor) for valor in data.values()])
    sql = """ INSERT INTO edificio (
        id, denominacion, otrasDenominaciones, categorias, tipologia, centro,
        ubicacionActual, acceso, formaDeIngreso, procedencia, volumen,
        cronologia, autores, descripcion, historia, objetoDocumento, tecnicas,
        signatura, exposicion, thumbnail) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """

    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido insertar el registro'
            
    con.commit()
        
    return redirect(url_for('index'))
