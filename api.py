from flask import *
import sqlite3
import json

'''Realización de los imports, en esta APIres haremos uso del framework
"Flask", gestionaremos la base de datos con "Sqlite3", y por último,
realizaremos la importación de los archivos JSON con su respectivo módulo.'''

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()							'''Conexión con la BD, el cursor y FLask.'''
app = Flask(__name__)


'''La base de datos utlizada es sobre arquitectos y edificios.'''


def devolver_atrib_arquitecto():	'''Devolución de atributos de tabla "arquitecto".'''
    return [
        'arquitecto',
        'num_colegio'
    ]


def devolver_atrib_edificio():	'''Devolución de atributos de la tabla "edificio".'''
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
			
'''Esta función nos permitirá mapear, o mostrar
   en la web la información de los registros.'''

    for fila in buffer_temporal:				
        registro = {}
        i = 0
        while i < len(fila):
            registro[atributos_tabla[i]] = fila[i]
            i += 1

        registros.append(registro)

    return registros



@app.route("/")	''' Definición de la ruta raíz, o path.'''
def index():	

'''Esta función va a mostrar mediante la sentencia SELECT y con laasistencia de
las funciones de devolución de atributos, los datos de arquitecto y edificio.'''

    atributos_arquitecto = devolver_atrib_arquitecto()	
    atributos_edificio = devolver_atrib_edificio()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)

    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode([arquitectos, edificios]), mimetype='application/json')	
    
    '''Finalmente, nos devolverá un JSON con la información'''
    
@app.route("/Edificio")	'''Definición de la ruta Edificio, la cual va a contener toda la información de la tabla edificio.'''
def index_edificio():

'''Función que nos mostrará los datos e información de edificio,
usando la sentencia SELECT y las funciones de devolución de atributos.'''

    atributos_edificio = devolver_atrib_edificio()
    cur.execute("SELECT * FROM edificio")
    edificios = mapear_registros(atributos_edificio, cur)
    
    return Response(json.JSONEncoder().encode(edificios), mimetype='application/json')


@app.route("/Arquitecto")	'''Definición de la ruta Arquitecto, contendrá toda la información de la tabla arquitecto.'''
def index_arquitecto():	

'''Función que nos mostrará los datos e información de edificio,
usando la sentencia SELECT y las funciones de devolución de atributos.'''

    atributos_arquitecto = devolver_atrib_arquitecto()

    cur.execute("SELECT * FROM arquitecto")
    arquitectos = mapear_registros(atributos_arquitecto, cur)
    
    return Response(json.JSONEncoder().encode(arquitectos), mimetype='application/json')


@app.route("/Edificio/eliminar/<id>")

'''Definición de la ruta Eliminar Edificio, en
esta ruta se va a eliminar por fila los edificios.'''

def eliminar_edificio(id):			
    
    parametros = (id,)
    sql = "DELETE FROM edificio WHERE id = ?;"	'''Se hará uso de la sentencia DELETE para eliminar edificios por id.'''
    
    							'''Por último, se ofrecerá un feedback mínimo mediante el uso de excepciones.'''
    try:
        cur.execute(sql, parametros)
        con.commit()
    except:
        return 'No se ha podido eliminar el registro'

    return redirect(url_for('index'))


@app.route("/Arquitecto/eliminar/<arquitecto>")	

'''Definición de la ruta Eliminar Arquitecto, en
esta ruta se va a eliminar por fila los arquitectos.'''

def eliminar_arquitecto(arquitecto):			

    parametros = (arquitecto,)
    sql = "DELETE FROM arquitecto WHERE arquitecto = ?;"
    	
    '''Al igual que la anterior función, esta se centrará
    en eliminar filas, en este caso de arquitectos.'''
    
    try:
        cur.execute(sql, parametros)
        con.commit()
    except:
        return 'No se ha podido eliminar el registro'

    return redirect(url_for('index'))				'''Finalmente, nos redirigirá al index.'''


@app.route('/Edificio/buscar/<denominacion>')

'''Definición de la ruta Buscar Edificio, esta ruta 
os permite realizar la búsqueda de un edificio.'''

def buscar_edificio(denominacion):

    '''Esta función permite realizar la búsqueda de
    un registro mediante el nombre del proyecto'''

    atributos_edificio = devolver_atrib_edificio()
    
    try:
        cur.execute('''SELECT * FROM edificio WHERE denominacion LIKE '%{}%' '''.format(denominacion))
    except:
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_edificio, cur)	
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')


@app.route('/Arquitecto/buscar/<arquitecto>')	
	
'''Definición de la ruta Buscar Arquitecto, esta ruta nos
permite realizar la búsqueda de arquitectos.'''

def buscar_arquitecto(arquitecto):

    '''Esta función permite realizar la búsqueda de
    un registro mediante el nombre del proyecto'''

    atributos_arquitecto = devolver_atrib_arquitecto()
    
    try:
        cur.execute('''SELECT * FROM arquitecto WHERE arquitecto LIKE '%{}%' '''.format(arquitecto))
    except:													 
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_arquitecto, cur)
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')


@app.route('/Edificio/modificar', methods=['GET', 'POST']) 	

'''Definición de la ruta Modificar Edificio, esta ruta nos permite modificar.'''

def modificar_edificio():						'''Los valores de los atributos de una fila de edificio.'''
    con = sqlite3.connect('database.db', check_same_thread=False)
    
    if request.method == 'GET':
    
    '''Nos apoyaremos en los verbos del protocolo http, usando GET y POST.
    GET nos añadirá los datos codificados a la URL y POST añadirá los datos
    al cuerpo, y no a la URL.'''
    
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
            
            '''Cuando se ejecute la sentencia UPDATE, se actualizarán
            los datos de la BD y nos va a redirigir al index.'''
            
            try:
                cur.execute(sql, parametros)
            except:
                return 'No se ha podido actualizar el registro'
            
        con.commit()
        
        return redirect(url_for('index'))    


@app.route('/Arquitecto/modificar', methods=['GET', 'POST'])

'''Definición de la ruta Modificar Arquitecto, la cual nos
permitirá modificar los datos de las filas de la tabla arquitecto.'''

    con = sqlite3.connect('database.db', check_same_thread=False)
    
    if request.method == 'GET':
    
    '''Nos va a hacer visible en la web los datos que modifiquemos.'''
    
        atributos_arquitecto = devolver_atrib_arquitecto()
        try:
            cur.execute('''SELECT * FROM arquitecto WHERE arquitecto={}'''.format(request.args.get('arquitecto')))
        except:
            return 'No se ha podido realizar la búsqueda'	
            
            '''Después de ejecutar la sentencia SELECT, nos va
            a mostrar los datos de la tabla arquitectos en la BD.'''

        busqueda = mapear_registros(atributos_arquitecto, cur)
        con.commit()

        return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')
        
        '''Nos devolverá una vista del JSON con los valores actualizados.'''
												
    elif request.method == 'POST':
        data = json.loads(request.data)
        
         '''Nos va a modificar los valores en el cuerpo pero no en la URL.'''

        for atributo, nuevo_valor in data.items():
            parametros = (nuevo_valor, data['arquitecto'])
            sql = '''UPDATE arquitecto set {} = ? WHERE arquitecto = ?'''.format(atributo)	
            
            '''Después de ejecutar la sentencia UPDATE, nos va a actualizar los
            datos de la tabla arquitecto en la BD y nos va a redirigir al index.'''
            
            try:							
                cur.execute(sql, parametros)
            except:
                return 'No se ha podido actualizar el registro'
            
        con.commit()
        
        return redirect(url_for('index'))

@app.route('/Arquitecto/anadir', methods=['POST'])

'''Definición de la ruta Añadir Arquitecto, la cual
nos permitirá realizar adiciones de filas de la tabla
arquitecto.'''

def anadir_arquitecto():				
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
        
    return redirect(url_for('index'))		'''Se nos redirigirá al index.'''

        
@app.route('/Edificio/anadir', methods=['POST'])

'''Definición de la ruta Añadir Edificio, la cual nos
permitirá realizar adiciones por fila a la tabla edificio.'''

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
        
        '''Se ejecutará la sentencia INSERT para añadir a los
        valores a los atributos de la tabla edificio.'''
        
    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido insertar el registro'
            
    con.commit()
        
    return redirect(url_for('index'))		'''Se nos redirigirá al index.'''
