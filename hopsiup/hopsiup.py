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
    return render_template('show_links.html', links=links)

@app.route('/add', methods=['POST'])
def add_link():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into links (link, title, user_id) values (?, ?)',
                 [request.form('url'), request.form['title'], request.form['user_id']])

if __name__ == '__main__':
    app.run()
