import sqlite3
from flask import Flask, request, session, g, redirect \
     abort, render_template, flash

# configuration
DATABASE = '/tmp/hopsiup.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
