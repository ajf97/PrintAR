from flask import Flask, render_template, session, request, redirect, url_for
from pickleshare import *
import os

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = PickleShareDB('./db')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    if 'username' in session:
        models = os.listdir('static/models')
        return render_template('dashboard.html',files=models)
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in db and password == db[username]['password']:
            session['username'] = request.form['username']
            session['name'] = db[username]['name']
            session['email'] = db[username]['email']
            return redirect(url_for('dashboard'))
        else:
            error = 'Usuario o contraseña incorrectos'
            return render_template('index.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/camera.html')
def camera():
    return render_template('camera.html')


@app.route('/object/<file>')
def show_object(file):
    return render_template('camera.html', file=file)


@app.route('/profile.html')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('index'))


@app.route('/update_profile.html', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        return redirect(url_for('index'))
    elif request.method == 'GET' and session['username']:
        return render_template('update_profile.html')
    elif request.method == 'POST' and session['username']:
        username = session['username']

        db[username]['email'] = request.form['email']
        db[username]['password'] = request.form['password']
        db[username]['name'] = request.form['name']
        db[username] = db[username]  # Para forzar que se guarde en db

        session['name'] = db[username]['name']
        session['email'] = db[username]['email']

        return redirect(url_for('index'))


@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'GET' and 'username' not in session:
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']

        if username not in db:
            db[username] = dict()
            db[username]['email'] = request.form['email']
            db[username]['password'] = request.form['password']
            db[username]['name'] = request.form['name']
            db[username] = db[username]  # Para forzar que se guarde en db
            return redirect(url_for('index'))
        else:
            error = 'El usuario ya existe'
            return render_template('signup.html', error=error)

    elif session['username']:
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html')


if __name__ == "__main__":
    app.run(ssl_context='adhoc')