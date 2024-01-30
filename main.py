import pymysql
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/home')
def index():
    return render_template("index.html.jinja")