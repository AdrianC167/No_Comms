from flask import Flask
from flask import render_template,request, redirect
import pymysql
import pymysql.cursors
import flask_login

app = Flask(__name__)
app.secret_key = "idfidhjifgd_@fjhdfds_Fdnfj@jndDFjidERFD0u8ss@!#$#@fdfjkDSfh__hn`jdjf^$23##@!ihjvdjp6HYJfdshn_adjshfskadsnabfhgrhbeyhfsdgf7%&jgrfhhgnjdsf_fhdjfhj<cvhfihufsf>djhfhbfjs#2mjfndihsknjnfdT^$3fDSFdsFdsffdnhogjithYJuFdvTYybyoknD_gjnfjGTGFVR#$Rg,s5egojfSFvhbtggRFSHJG$#42gS2:sd;}#@P}"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
     is_authenticated = True
     is_anonymous = False
     is_active = True
     def __init__(self, id, username, email,profile_image):
          self.id = id
          self.username = username
          self.email = email
          self.profile_image = profile_image
     def get_id(self):
      return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `User_id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    conn.commit()
    if result is None:
        return None
    
    return User(result['User_id'], result['Username'],result['Email'],result['Profile Image'])

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

    try:
        if request.method == 'POST':
                username = request.form["username"]
                password = request.form["password"]
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM `users` WHERE `Username` = '{username}' ")
                result = cursor.fetchone()  
                cursor.close()
                conn.commit()
                if password == result['Password']:
                    user = load_user(result['User_id'])
                    flask_login.login_user(user)
                    return redirect('/feed')  
    except TypeError:
        return "Wrong Username or Password"    

    return render_template('signin.html.jinja')


@app.route('/feed', methods=['GET','POST'])
@flask_login.login_required
def feed():

    return render_template('feed.html.jinja')