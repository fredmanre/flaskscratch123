from flask import Flask, render_template, logging, url_for, redirect, session, flash, request
from data import Articles
# from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL


app = Flask(__name__)

# Config Mysql Server

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'fredmanre'
app.config['MYSQL_PASSWORD'] = 'perrodeagua'
app.config['MYSQL_DB'] = 'flaskscratch'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init mysqldb
mysql = MySQL(app)

Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=6, max=100)])
    username = StringField('Username', [validators.Length(min=5, max=30)])
    email = StringField('Email', [validators.Length(min=10, max=60)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Confirm', message="Passwords do not match")
    ])
    confirm = PasswordField('Confirm password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.name.data
        email = form.email.data
        password = sha256_crypt(str(form.password.data))
        # creamos un cursor
        cur = mysql.connection.cursor()
        cur.execute(
            "insert into users(name, username, password, email) values({}, {}, {}, {})")
        return render_template('register.html')
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
