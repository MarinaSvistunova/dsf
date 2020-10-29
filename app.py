import csv
import os.path
import sqlite3

from flask import Flask, url_for, g
from flask import render_template
from flask import request, flash

from FDataBase import FDataBase

from wtforms import Form, BooleanField, StringField, PasswordField, validators


# конфигурация
DATABASE = '/tmp/iito.db'
DEBUG = True
SECRET_KEY = 'jvnp[oasmf#4jlavn%$!3]6;fdljvaoiubvcqwu'

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    surname = StringField('Surname', [validators.Length(min=4, max=50)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ioahcvjneklqivuhuibefcuiaevjcnelariochjvndolkaiorshnkrei'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'iito.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row # представление не в виде кортежа, а в виде словаря
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('iito.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.sq_db = connect_db()
    return g.sq_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.iito.close()

@app.route('/', methods=['GET', 'POST'])
def main_route():
    form = RegistrationForm(request.form)
    db = get_db()

    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['surename']) > 3:
            res = dbase.addReg(request.form['name'], request.form['surename'], request.form['email'])
            # with open("registration.csv", "a", newline="") as file:
            #     user = [request.form['name'], request.form['surename'], request.form['email']]
            #     writer = csv.writer(file)
            #     writer.writerow(user)
            if not res:
                flash('Fall', category="error")
            else:
                flash('OK', category="success")
        else:
            flash('Fall', category="error")

    return render_template('layout.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
