from flask import render_template
import pymysql
from db import app

class Database:
    def __init__(self):
        host = app.config.get('DB_IP')
        user = app.config.get('DB_USER')
        db = 'fpl'
        self.con = pymysql.connect(host=host, user=user, \
                                   db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

@app.route('/')
def index():
    db = Database()
    db.cur.execute("SELECT * FROM players")
    res = db.cur.fetchall()
    return render_template('index.html', result=res)
