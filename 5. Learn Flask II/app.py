from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from psycopg2.extras import DictCursor
import psycopg2
from functools import wraps

app = Flask(__name__)
con = psycopg2.connect(
    host='localhost',
    port='5432',
    password='010202',
    user='postgres',
    database='flaskarticleapp'
)
cursor = con.cursor(cursor_factory=DictCursor)


artic = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    cursor.execute('SELECT * FROM public.articles')
    articles = cursor.fetchall()
    if cursor.rowcount > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Article Found'
        return render_template('articles.html', msg=msg)

@app.route('/articles/<string:id>/')
def article(id):
    cursor.execute('SELECT * FROM public.articles WHERE id = %s', [id])
    article = cursor.fetchone()
    return render_template('article.html', article=article)

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

        cursor.execute('SELECT * FROM public.users WHERE username = %s', [username])
        data = cursor.fetchone()

        if data is not None:
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'succes')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
        cursor.close()
        con.close()
    
    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cursor.execute('SELECT * FROM public.articles WHERE author = %s', [session['username']])
    articles = cursor.fetchall()
    if cursor.rowcount > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Article Found'
        return render_template('dashboard.html', msg=msg)

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cursor.execute('INSERT INTO public.articles(title, body, author) VALUES (%s, %s, %s)', (title, body, session['username']))

        con.commit()

        cursor.close()
        con.close()
        flash('Article Created', 'succes')

        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cursor.execute("SELECT * FROM public.articles WHERE id = %s", [id])
    article = cursor.fetchone()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cursor.execute('UPDATE articles SET title=%s, body=%s WHERE id=%s', (title, body, id ))

        con.commit()
        flash('Article Updated', 'succes')

        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cursor.execute('DELETE FROM articles WHERE id = %s', [id])
    con.commit()
    flash('Article Deleted', 'succes')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(port=5002, debug=True)
