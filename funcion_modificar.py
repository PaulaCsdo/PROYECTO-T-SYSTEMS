from flask import *
import sqlite3


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


def buscar_edificio(id):
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

    parametros = (id,)
    sql = '''SELECT * FROM edificio WHERE id='?''''
    
    try:
        cur.execute(sql, parametros)
    except:
        return 'No se ha podido realizar la búsqueda'

    busqueda = mapear_registros(atributos_edificio, cur)
    con.commit()

    return Response(json.JSONEncoder().encode(busqueda), mimetype='application/json')


def modificar:
    @app.route('/modificar', methods=['GET', 'POST'])
    
    #recogemos la id del edificio por la id que pasamos por la url
    if request.method == 'GET':
        buscar(request.args.get('id'))

    #recogemos los datos del formulario por POST
##    if request.method == 'POST':
##        acceso = request.form.get('acceso')
##        thumbnail = request.form.get('thumbnail')
##        procedencia = request.form.get('procedencia')
##        volumen = request.form.get('volumen')
##        denominacion = request.form.get('denominacion')
##        cronologia = request.form.get('cronologia')
##        otras_denominaciones = request.form.get('otras_denominaciones')
##        autores = request.form.get('autores')
##        categoria = request.form.get('categoria')
##        descripcion = request.form.get('descripcion')
##        tipologia = request.form.get('tipologia')
##        historia = request.form.get('historia')
##        exposicion = request.form.get('exposicion')
##        centro = request.form.get('centro')
##        objeto_documento = request.form.get('objeto_documento')
##        ubicacion_habitual = request.form.get('ubicacion_habitual')
##        tecnicas = request.form.get('tecnicas')
##        signatura = request.form.get('signatura')
##        forma_de_ingreso = request.form.get('forma_de_ingreso')
        parametros = []
        if request.method == 'POST':
            for campo in request.form.values():
                parametros.append(campo)
                
        
        #creamos la conexion a la bd y el cursor para ejecutar la sentencia sql
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        
        #actualizamos los datos donde coincide el id
##        cur.execute('''UPDATE edificios
##        set acceso = {}, thumbnail = {}, procedencia = {}, volumen = {},
##        denominacion = {}, cronologia = {}, otras_denominaciones = {}, autores = {}, categoria = {}, descripcion = {},
##        tipologia = {}, historia = {}, exposicion = {}, centro = {}, objeto_documento = {}, ubicacion_habitual = {},
##        tecnicas = {}, signatura = {}, forma_de_ingreso = {}
##        where id = {}'''.format(acceso,thumbnail,procedencia,volumen,denominacion,
##        cronologia,otras_denominaciones,autores,categoria,descripcion,tipologia,historia,exposicion,centro,objeto_documento,
##        ubicacion_habitual,tecnicas,signatura,forma_de_ingreso,edificio_id))

        sql = '''UPDATE edificios
        set acceso = ?, thumbnail = ?, procedencia = ?, volumen = ?,
        denominacion = ?, cronologia = ?, otras_denominaciones = ?, autores = ?, categoria = ?, descripcion = ?,
        tipologia = ?, historia = ?, exposicion = ?, centro = ?, objeto_documento = ?, ubicacion_habitual = ?,
        tecnicas = ?, signatura = ?, forma_de_ingreso = ?
        where id = ?'''
        cur.execute(sql, tuple(parametros))
        

        con.commit()
        con.close()
        
        #volvemos al index para ver los cambios
        redirect(url_for('index'))
    
