from flask import request
import sqlite3

def modificar:
    @app.route('/modificar', methods=['GET', 'POST'])
    
    '''recogemos la id del edificio por la id que pasamos por la url'''
    if request.method == 'GET':
        edificio_id = request.args.get('id')

    '''recogemos los datos del formulario por POST'''
    if request.method == 'POST':
        acceso = request.form.get('acceso')
        thumbnail = request.form.get('thumbnail')
        procedencia = request.form.get('procedencia')
        volumen = request.form.get('volumen')
        denominacion = request.form.get('denominacion')
        cronologia = request.form.get('cronologia')
        otras_denominaciones = request.form.get('otras_denominaciones')
        autores = request.form.get('autores')
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        tipologia = request.form.get('tipologia')
        historia = request.form.get('historia')
        exposicion = request.form.get('exposicion')
        centro = request.form.get('centro')
        objeto_documento = request.form.get('objeto_documento')
        ubicacion_habitual = request.form.get('ubicacion_habitual')
        tecnicas = request.form.get('tecnicas')
        signatura = request.form.get('signatura')
        forma_de_ingreso = request.form.get('forma_de_ingreso')
        
        '''creamos la conexion a la bd y el cursor para ejecutar la sentencia sql'''
        database = 'database.db'
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        
        '''actualizamos los datos donde coincide el id'''
        cur.execute('''UPDATE edificios
        set acceso = {}, thumbnail = {}, procedencia = {}, volumen = {},
        denominacion = {}, cronologia = {}, otras_denominaciones = {}, autores = {}, categoria = {}, descripcion = {},
        tipologia = {}, historia = {}, exposicion = {}, centro = {}, objeto_documento = {}, ubicacion_habitual = {},
        tecnicas = {}, signatura = {}, forma_de_ingreso = {}
        where id = {}'''.format(acceso,thumbnail,procedencia,volumen,denominacion,
        cronologia,otras_denominaciones,autores,categoria,descripcion,tipologia,historia,exposicion,centro,objeto_documento,
        ubicacion_habitual,tecnicas,signatura,forma_de_ingreso,edificio_id))

        con.commit()
        con.close()
        
        '''volvemos al index para ver los cambios'''
        redirect('/')
    
