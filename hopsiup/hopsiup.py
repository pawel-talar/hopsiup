import sqlite3
from flask import Flask, request, session, g, redirect, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object('init')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()
