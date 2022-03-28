import json
import requests
import sqlite3

### No funciona debido a la lentitud de resolucion de DNS
##
##def descargar_json(url):
##    return requests.get(url).text
##
##datos = json.loads(descargar_json('http://datos.unican.es/patrimonio/108/Patrimonio_arquitectonico.json'))


def leer_json(archivo):
    f = open(archivo, encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


datos = leer_json('patrimonio.json')
DATABASE = 'database.db'

con = sqlite3.connect(DATABASE)
cur = con.cursor()

cur.execute('''
    CREATE TABLE arquitecto (
        arquitecto text,
        num_colegio integer,

        primary key(arquitecto),
        unique(num_colegio)
    );
''')

cur.execute('''
CREATE TABLE edificio (
    id text,
    denominacion text,
    otrasDenominaciones text,
    categorias text,
    tipologia text,
    centro text,
    ubicacionActual text,
    acceso text,
    formaDeIngreso text,
    procedencia text,
    volumen text,
    cronologia text,
    autores text,
    descripcion text,
    historia text,
    objetoDocumento text,
    tecnicas text,
    signatura text,
    exposicion text,
    thumbnail text,

    foreign key (autores) references arquitecto(arquitecto),
    primary key (id)
);
''')

i = 101
arquitectos = []

for reg in datos:
    if reg['Autores'] not in arquitectos:
        arquitectos.append(reg['Autores'])
        valores = (reg['Autores'], i)
        cur.execute('''
        INSERT INTO arquitecto VALUES(?, ?)
        ''', valores)
        i += 1
    
    valores = (reg['id'], reg['Denominacion'], reg['OtrasDenominaciones'],
               reg['Categoria'], reg['Tipologia'], reg['Centro'],
               reg['UbicacionHabitual'], reg['Acceso'], reg['FormaDeIngreso'], reg['Procedencia'],
               reg['Volumen'], reg['Cronologia'], reg['Autores'],
               reg['Descripcion'], reg['Historia'], reg['ObjetoODocumento'],
               reg['Tecnicas'], reg['Signatura'], reg['Exposicion'],
               reg['Thumbnail'])
    cur.execute('''
    INSERT INTO edificio VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', valores)
    

con.commit()
con.close()
    


    

