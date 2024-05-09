from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import psycopg2

app = Flask(__name__)
con = psycopg2.connect(
    host='localhost',
    port='5432',
    password='010202',
    user='postgres',
    database='flaskarticleapp'
)
cursor = con.cursor()


artic = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=artic)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cursor.execute("INSERT INTO public.users(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))
        con.commit()
        cursor.close()
        con.close()

        flash('You are now registered and you can log in', 'succes')

        redirect(url_for('index'))

        return render_template('register.html', form = form)
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        result = cursor.execute('SELECT * FROM public.users WHERE username = %s', [username])
        
        if result > 0:
            data = cursor.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'succes')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            cursor.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(port=5002, debug=True)
