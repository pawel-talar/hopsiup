import sqlite3
from flask import Flask, request, session, g, redirect, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object('init')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_main():
    data = g.db.execute('select l.title, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(title=row[0], user=row[1]) for row in data.fetchall()]
    return render_template('layout.html', links=links)

@app.route('/add', methods=['POST'])
def add_link():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into links (link, title, user_id) values (?, ?)',
                 [request.form('url'), request.form['title'], request.form['user_id']])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = g.db.execute('select login, password from users')
        users_from_db = [dict(login=row[0], password=row[1])\
                for row in data.fetchall()]
        if a not in users_from_db:
            error = 'Invalid username'
        elif users_from_db[a] != password:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_main'))

if __name__ == '__main__':
    app.run()
