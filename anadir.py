from flask import Flask, Response
import sqlite3

def aniadir_arquitectos (arquitecto, num_colegio):

    try:

        con = sqlite3.connect('/home/tsi/Documentos/PROYECTO-T-SYSTEMS/database.db')
        print("La base de datos está conectada \n")
        cur = con.cursor()
        App = Flask(__name__)

        parametros_ar = (arquitecto, num_colegio)
        query_insert = """ INSERT INTO arquitecto (arquitecto, num_colegio) 
                          VALUES (?, ?) """

        
        cur.execute(query_insert, parametros_ar)
        con.commit()
        print("Valores añadidos y guardados ", cur.rowcount)

        cur.close()

    except sqlite3.Error as error:
        print("Los valores no se han añadido a la tabla \n", error)

def aniadir_edificios (

    id, denominacion, otrasDenominaciones, categorias, tipologia, centro,
    ubicacionActual, acceso, formaDeIngreso, procedencia, volumen,
    cronologia, autores, descripcion, historia, objetoDocumento, tecnicas,
    signatura, exposicion, thumbnail
    
    ):

    try:

        con = sqlite3.connect('/home/tsi/Documentos/PROYECTO-T-SYSTEMS/database.db')
        print("La base de datos está conectada \n")
        cur = con.cursor()
        App = Flask(__name__)

        parametros_ed = (

            id, denominacion, otrasDenominaciones, categorias, tipologia, centro,
            ubicacionActual, acceso, formaDeIngreso, procedencia, volumen,
            cronologia, autores, descripcion, historia, objetoDocumento, tecnicas,
            signatura, exposicion, thumbnail

        )

        query_insert = """ INSERT INTO edificio (

            id, denominacion, otrasDenominaciones, categorias, tipologia, centro,
            ubicacionActual, acceso, formaDeIngreso, procedencia, volumen,
            cronologia, autores, descripcion, historia, objetoDocumento, tecnicas,
            signatura, exposicion, thumbnail

        ) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """

        
        cur.execute(query_insert, parametros_ed)
        con.commit()
        print("Valores añadidos y guardados ", cur.rowcount)

        cur.close()

    except sqlite3.Error as error:
        print("Los valores no se han añadido a la tabla \n", error)

## Definición de parámetros:

aniadir_arquitectos('', 0)
aniadir_edificios('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',)