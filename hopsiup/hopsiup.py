import os
import sqlite3
from flask import Flask, request, session, g, redirect, \
    abort, render_template, flash, url_for
from flask.ext import assets

app = Flask(__name__)
app.config.from_object('init')

env = assets.Environment(app)

env.load_path = [
    os.path.join(os.path.dirname(__file__), 'coffee'),
    os.path.join(os.path.dirname(__file__), 'bower_components'),
]

env.register(
    'js_all',
    assets.Bundle(
        'jquery/dist/jquery.min.js',
        assets.Bundle(
            'all.coffee',
            filters=['coffeescript']
        ),
        output='js_all.js'
    )
)

env.register(
    'css_all',
    assets.Bundle(
        'bootstrap/dist/css/bootstrap.min.css',
        output='css_all.css'
    )
)


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
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('show_links.html', links=links)


@app.route('/mikroblog')
def show_blog():
    return render_template('show_posts.html')

@app.route('/waiting')
def show_waiting():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('show_waiting_links.html', links=links)

@app.route('/user_area')
def user_area():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_area.html', links=links)

@app.route('/user')
def user_account():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_account.html', links=links)


@app.route('/articles_stat')
def user_articles_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_articles.html', links=links)


@app.route('/blog_stat')
def user_blog_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_blog.html', links=links)


@app.route('/social_stat')
def user_social_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' + \
                        'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_social.html', links=links)


@app.route('/l/<id>')
def show_link_page(id=None):
    data = g.db.execute('select l.lpoints, l.link, l.title, l.description, u.login from links as l,' +
                        'users as u on l.user_id == u.user_id where l.link_id={0}'.format(id))
    link_infos = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], author=row[4]) for row in data.fetchall()]
    return render_template('link_page.html', link_info=link_infos[0])

@app.route('/messages')
def messages():
    data = g.db.execute('select content, sent_on from messages ' +
                        'where to_uid = {0}'.format(session['uid']))
    messages_to = [dict(content=row[0], date=row[1]) for row in data.fetchall()]
    data2 = g.db.execute('select user_id, login from users where user_id != {0}'.format(session['uid']))
    users = [dict(id=row[0], login=row[1]) for row in data2.fetchall()]
    return render_template('messages.html', messages=messages_to, users=users)

@app.route('/add')
def add_link():
    return render_template('add_link.html')

@app.route('/register')
def register():
    return render_template('register.html')

def register_user(username, password):
    g.db.execute('insert into users (login, password) values (?, ?)',
                 [username, password])
    g.db.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = g.db.execute('select user_id, login, password from users')
        users_from_db = [dict(uid=row[0], login=row[1], password=row[2]) \
                         for row in data.fetchall()]
        print(users_from_db)
        for row in users_from_db:
            if row["login"] == username and row["password"] == password:
                session['logged_in'] = True
                session['user'] = username
                session['uid'] = row["uid"]
                flash('Zalogowano pomyslnie!')
                return redirect(url_for('show_main'))
        register_user(username, password)
        session['logged_in'] = True
        session['user'] = username
        flash('Zalogowano pomyslnie!')
        return redirect(url_for('show_main'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_main'))


@app.route('/ranking')
def ranking():
    data = g.db.execute('select login, upoints from users order by upoints desc')
    users = [dict(login=row[0], points=row[1]) for row in data.fetchall()]
    return render_template('ranking.html', users=users)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
