from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, email, password):
         self.id = id
         self.email = email
         self.password = password
         self.authenticated = False
         def is_active(self):
            return self.is_active()
         def is_anonymous(self):
            return False
         def is_authenticated(self):
            return self.authenticated
         def is_active(self):
            return True
         def get_id(self):
            return self.id
         
@app.route("/login")
def login():
    #check if already logged in- if so send home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template("login.html")
         
@app.route('/login', methods=["POST"])
def login_post():

    # do the standard database stuff and find the user with email
    con = sqlite3.connect("login.db")
    curs = con.cursor()
    email= request.form['email']
    curs.execute("SELECT * FROM login where email = (?)", [email])
#return the first matching user then pass the details to
#create a User object – unless there is nothing returned then flash a message
    row=curs.fetchone()
    if row==None:
        flash('Please try logging in again')
        return render_template('login.html')
    user = list(row);     
    liUser = User(int(user[0]),user[1],user[2])
    password = request.form['password']
    match = liUser.password==password
#if our password matches- run the login_user method
    if match and email==liUser.email:
        login_user(liUser,remember=request.form.get('remember'))
        flash(f'You have been logged in {liUser.email}')
        return redirect(url_for('home'))
    else:
        flash('Please try logging in again')
        return render_template('login.html')
    return render_template('home.html')




@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * from login where user_id = (?)",[user_id])
    liUser = curs.fetchone()
    if liUser is None:
        return None
    else:
        return User(int(liUser[0]), liUser[1], liUser[2])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template("register.html")
    
@app.route("/adduser", methods=["POST"])
def adduser():
    if request.method == "POST":
        values = (request.form["email"], request.form["password"])
        con = sqlite3.connect("login.db")
        cur = con.cursor()
        cur.execute("INSERT INTO login (email, password) VALUES (?,?)", values)
        con.commit()
        con.close
        flash("Successfully registered!")
        return redirect(url_for("login"))
    flash("An error ocurred please try again")
    return redirect(url_for("home"))
        

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("home_loggedin.html")
    else:
        return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)