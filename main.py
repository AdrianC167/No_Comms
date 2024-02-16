from flask import Flask,g
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
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `User_id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()
    if result is None:
        return None
    
    return User(result['User_id'], result['Username'],result['Email'],result['Profile Image'])

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="achen",
        password="232126110",
        database="achen_no_comms",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
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
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users`(`Email` , `Password`, `Name`, `User_Bio`, `Username`,`Pronoun`,`Birthday`) VALUES('{email}', '{password}', '{name}', '{bio}', '{username}','{pronoun}', '{birthday}')")         
        cursor.close()
        get_db().commit()
    
    if flask_login.current_user.is_authenticated:
            return redirect('/feed') 
    return render_template('signup.html.jinja')


@app.route('/signin', methods=['GET','POST'])
def signin():

    try:
        if request.method == 'POST':
                username = request.form["username"]
                password = request.form["password"]
                cursor = get_db().cursor()
                cursor.execute(f"SELECT * FROM `users` WHERE `Username` = '{username}' ")
                result = cursor.fetchone()  
                cursor.close()
                get_db().commit()
                if password == result['Password']:
                    user = load_user(result['User_id'])
                    flask_login.login_user(user)
                    return redirect('/feed')          
            
        if flask_login.current_user.is_authenticated:
            return redirect('/feed')  
    except TypeError:
        return "Wrong Username or Password"  



    return render_template('signin.html.jinja')


@app.route('/feed', methods=['GET','POST'])
@flask_login.login_required
def feed():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM `post` ORDER BY `timestamp` DESC')
    results = cursor.fetchall()
    cursor.close()
    #return flask_login.current_user
    return render_template('feed.html.jinja',post_list = results)


@app.route('/post', methods = ["POST"])
@flask_login.login_required
def create_post():
    description = request.form['description']
    user_id = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"INSERT INTO `post`(`description`, `User_id`) VALUES ('{description}','{user_id}')")
    get_db().commit()
    return redirect("/feed")


@app.route('/likes/<int:post_index>', methods = ['POST'])
def likes(post_index):
    cursor = get_db().cursor()
    cursor.execute(f"UPDATE `post` SET `likes` = `likes` + 1  WHERE `id` = {post_index} ")
    cursor.close()
    get_db().commit()
    return redirect('/feed')