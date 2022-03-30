
from flask import *
import sqlite3
import json


# Conexión con la BD, el cursor y flask.
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()							
app = Flask(__name__)


# Funciones auxiliares
def devolver_atrib_arquitecto():
    '''Devuelve una lista con los atributos de un arquitecto'''
    
    return [
        'arquitecto',
        'num_colegio'
    ]


def devolver_atrib_edificio():
    '''Devuelve una lista con los atributos de un edificio'''
    
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


def mapear_registros(atributos_tabla, buffer_temporal):			
    '''Recibidos los atributos de una tabla (lista) y un buffer de datos
    (cursor sqlite3) devuelve una lista con los registros del buffer en
    en formato de diccionario'''

    for fila in buffer_temporal:				
        registro = {}
        i = 0
        while i < len(fila):
            registro[atributos_tabla[i]] = fila[i]
            i += 1

        registros.append(registro)

    return registros

def abrir_bd():
    


# Definición de los end points de la API
@app.route("/")
def index():	
    '''Devuelve un array formado por dos arrays de json con los
    datos de arquitectos y edificios, respectivamente'''

    atributos_arquitecto = devolver_atrib_arquitecto()	
    atributos_edificio = devolver_atrib_edificio()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)

    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode([arquitectos, edificios]), mimetype='application/json')	

    
@app.route("/Edificio")
def index_edificio():
    '''Devuelve un array de json con los datos de todos los edificios de la bd'''

    atributos_edificio = devolver_atrib_edificio()
    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode(edificios), mimetype='application/json')


@app.route("/Arquitecto")
def index_arquitecto():	
    '''Devuelve un array de json con los datos de todos los arquitectos de la bd'''

    atributos_arquitecto = devolver_atrib_arquitecto()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)
    
    return Response(json.JSONEncoder().encode(arquitectos), mimetype='application/json')


@app.route("/Edificio/eliminar/<id>")
def eliminar_edificio(id):			
    '''Recibe como parámetro el id del edificio a eliminar.
    Si el borrado es exitoso, redirige a la raíz'''
    
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
    '''Recibe como parámetro el nombre del arquitecto a eliminar.
    Si el borrado es exitoso, redirige a la raíz'''
    
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
    '''Devuelve un array de json cuyas denominaciones contienen
    el valor "denominacion"'''

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
     '''Devuelve un array de json cuyos arquitectos contienen
    en su nombre el valor "arquitecto" '''

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
    '''- Si el método de la peticion es GET y se pasa como parámetro (en la URL) el id de edificio DEVUELVE
            un json con los datos del edificio.
        - Si el método de la petición es POST y la información de la petición está codificada en json, entonces
            modifica la información del edificio y redirige al index'''
    
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
''' - Si el método de la peticion es GET y se pasa como parámetro (en la URL) el nombre (arquitecto)
        del arquitecto DEVUELVE un json con los datos del arquitecto.
    - Si el método de la petición es POST y la información de la petición está codificada en json,
        entonces modifica la información del arquitecto y redirige al index'''

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
    '''Habiendo enviado una petición por POST cuya información estuviera codificada en json
    añade el registro a la bd y redirige al index'''
    
    data = json.loads(request.data)
    atributos_arquitecto = devolver_atrib_arquitecto()
    
    parametros = (data['arquitecto'], data['num_colegio'])
    sql = """ INSERT INTO arquitecto (arquitecto, num_colegio) 	
                          VALUES (?, ?) """				
                          
                          '''Ejectuaremos la setencia INSERT para darle
                          valor alos atributos de arquitecto.'''

    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido insertar el registro'
            
    con.commit()
        
    return redirect(url_for('index'))

        
@app.route('/Edificio/anadir', methods=['POST'])
def anadir_edificio():
    '''Habiendo enviado una petición por POST cuya información estuviera codificada en json
    añade el registro a la bd y redirige al index'''
    
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
