from flask import Flask, Response, request
import sqlite3
import json

database = 'database.db'
con = sqlite3.connect('database.db')
cur = con.cursor()
app = Flask(__name__)


@app.route("/Edificio/eliminar/<id>")
def eliminar_edificio(id):
    cur.execute("DELETE FROM edificio WHERE id = {};".format(id))
    con.commit()
    con.close()

    return redirect(url_for('index'))


@app.route("/Arquitecto/eliminar/<arquitecto>")
def eliminar_arquitecto(arquitecto):
    cur.execute("DELETE FROM arquitecto WHERE arquitecto = {};".format(arquitecto))
    con.commit()
    con.close()

    return redirect(url_for('index'))

            

