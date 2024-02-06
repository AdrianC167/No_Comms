from flask import Flask
from flask import render_template,request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)

conn = pymysql.connect(
        database = "achen_no_comms",
        user = "achen",
        password = "232126110",
        host = "10.100.33.60",
        cursorclass = pymysql.cursors.DictCursor
 )

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        name = request.form["Name"]
        bio = request.form["Bio"]
        username = request.form["Username"]
        pronoun = request.form["pronouns"]
        birthday = request.form["birthday"]
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `users`(`Email` , `Password`, `Name`, `User_Bio`, `Username`,`Pronoun`,`Birthday`) VALUES('{email}', '{password}', '{name}', '{bio}', '{username}','{pronoun}', '{birthday}')")         
        cursor.close()
        conn.commit()
    

    return render_template('signup.html.jinja')


@app.route('/signin', methods=['GET','POST'])
def signin():
    
    if request.method == 'POST' or 'GET':
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE `Username` = '{username}' ")
        user = cursor.fetchone()  
        cursor.close()
    if password == user['Password']:
        return redirect('/feed')

    return render_template('signin.html.jinja')
