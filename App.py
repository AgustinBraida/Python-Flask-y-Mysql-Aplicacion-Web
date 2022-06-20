from os import curdir
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conección a la base de datos.
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "1234567"
app.config["MYSQL_DB"] = "negocio"
mysql = MySQL(app)

#Configuraciones.
app.secret_key = 'mysecretkey'


# Mandamos los datos a la pagina principal
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientess')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)


# Agregamos los datos a la base de datos
@app.route('/add_contact/', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nom_apll = request.form['nombre_apellido']
        eml = request.form['email']
        tel = request.form['telefono']
        cur = mysql.connection.cursor()
        #Escribimos la consulta.
        cur.execute('INSERT INTO clientess (nombre_apellido, email, telefono) VALUES (%s, %s, %s)', (nom_apll, eml, tel))
        #Ejecutamos la consulta.
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente!!')
        return redirect(url_for('index'))


# Obtenemos los valores para luego modificarlos
@app.route('/get-contanto/<id>')
def get_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientess WHERE id = {0}'.format(id))
    datos = cur.fetchall()
    return render_template('update.html', contacto=datos[0])


# Actualizamos los datos en la base de datos
@app.route('/edit/<id>', methods=['POST'])
def edit_contact(id):
    if request.method == 'POST':
        nom_apll = request.form['nombre_apellido']
        eml = request.form['email']
        tel = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE clientess SET nombre_apellido = %s, email = %s, telefono = %s WHERE id = %s',(nom_apll, eml, tel, id))
        mysql.connection.commit()
        flash("Contacto editado satisfactoriamente!")
        return redirect(url_for('index'))


# Eliminamos una persona por su 'id'
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clientess WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash("Contacto eliminado satisfactoriamente!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
