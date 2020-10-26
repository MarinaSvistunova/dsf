import csv
import os.path

from flask import Flask, url_for
from flask import render_template
from flask import request

from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    surname = StringField('Surname', [validators.Length(min=4, max=50)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_route():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        with open("registration.csv", "a", newline="") as file:
            user = [request.form['name'], request.form['surename'], request.form['email']]
            writer = csv.writer(file)
            writer.writerow(user)
    return render_template('layout.html', form=form)

# @app.route('/', methods=['GET', 'POST'])
# def register():
#     items = []
#     form = RegistrationForm(request.form)
#
#     path = os.getcwd()
#     if os.path.exists(path + '/registration.csv'):
#
#         with open("registration.csv", "r") as file:
#             reader = csv.reader(file)
#
#             for row in reader:
#                 row = row[0].split(';')
#                 items += [[row[0], row[1], row[2]]]
#
#     if request.method == 'POST' and form.validate():
#         name, surname, email = form.name.data, form.surname.data, form.email.data
#
#         with open("registration.csv", "a", newline="") as file:
#
#             user = [name, surname, email]
#             writer = csv.writer(file)
#             writer.writerow(user)
#         items += [[]]
#         items[-1] = [name, surname, email]
#
#     return render_template('register.html', form=form, items=items)


if __name__ == '__main__':
    app.run()
