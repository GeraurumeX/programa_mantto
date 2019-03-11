from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL Connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mantto_equipos'
mysql.init_app(app)

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM equipos')
    data = cursor.fetchall()
    return render_template('index.html', equipments = data)

# Agregar equipos
@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        fecha_mantto_prog = request.form['fecha_mantto_prog']
        fecha_mantto_real = request.form['fecha_mantto_real']
        #cursor = mysql.get_db().cursor()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO equipos (name, location, fecha_mantto_prog, fecha_mantto_real) VALUES (%s, %s, %s, %s)', (name, location, fecha_mantto_prog, fecha_mantto_real))
        #mysql.connection.commit()
        conn.commit()
        conn.close()
        flash('Equipment Added Successfully')
        return redirect(url_for('Index'))

# Obtener equipo para editar
@app.route('/edit/<id>')
def get_equipment(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM equipos WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('edit_equipment.html', equipment = data[0])


# Update equipo
@app.route('/update/<id>', methods = ['POST'])
def update_equipment(id):
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        fecha_mantto_prog = request.form['fecha_mantto_prog']
        fecha_mantto_real = request.form['fecha_mantto_real']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE equipos
            SET name = %s,
                location = %s,
                fecha_mantto_prog = %s,
                fecha_mantto_real = %s
            WHERE id = %s
        """, (name, location, fecha_mantto_prog, fecha_mantto_real, id))
        conn.commit()
        conn.close()
        flash('Contact Update Successfully')
        return redirect(url_for('Index'))

# Borrar equipos
@app.route('/delete/<string:id>')
def delete_equipment(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipos WHERE id = {0}'.format(id))
    conn.commit()
    conn.close()
    flash('Equipment Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
