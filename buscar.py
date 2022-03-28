from flask import Flask, request, Response
import jason
import sqlite3

database = 'database.db'
con = sqlite3.connect('database.db')
cur = con.cursor()
app = Flask(__name__)


#Mapear registros
def mapear_registros(atributos_tabla, cursor):
    for fila in cursor:
        registros={}
        i=0
        while i<len(fila):
            registro[atributos_tabla[i]]=fila[i]
            i +=1

        registros.append (registro)
        
    return registros
    
#Buscador por nombre del proyecto/edificio
@app.route('/buscar/<denominacion>', methods='POST')
def buscar(denominacion):
    '''Esta función permite realizar la búsqueda de un registro
    mediante el nombre del proyecto'''

    denominacion = request.form.get('denominacion')
    
    cur.execute('''SELECT * FROM edificio WHERE denominacion LIKE '%{}%' '''.format(denominacion))
    busqueda = mapear_registros(denominacion, cur)

    return Response(json.JSONEncoder().encode(busqueda), mimetype('application/json') 

    con.commit()
    con.close()
