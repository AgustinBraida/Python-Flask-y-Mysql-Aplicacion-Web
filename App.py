from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conección a la base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "pilar"
app.config["MYSQL_DB"] = "negocio"
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from clientes')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nom_apll = request.form['nombre_apellido']
        eml = request.form['email']
        tel = request.form['telefono']
        cur = mysql.connection.cursor()
        #Escribimos la consulta
        cur.execute('INSERT INTO clientes (nombre_apellido, email, telefono) VALUES (%s, %s, %s)', (nom_apll, eml, tel))
        #Ejecutamos la consulta
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente!!')
        return redirect(url_for('index'))

    

@app.route('/edit')
def edit_contact():
    return "Editar Contactos"

@app.route('/delete')
def delete_contact():
    return "Borrar Contactos"


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
