import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
login_manager = LoginManager(app)
login_manager.login_view = "Login"

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

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']

            with sqlite3.connect('students.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city) VALUES (?,?,?)", (name, addr, city) )
                con.commit()
                msg = "Result of addition : Record successfully added,0"
            
        except:
            con.rollback()
            msg = "Result of addition : Failed to add record,1"
        finally:
            con.close()
            return listStudents(msg)

@app.route("/liststudents")
@login_required
def listStudents(msg=None):
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("studentlist.html", rows=rows, msg=msg)

@app.route("/searchrec", methods=["POST", "GET"])
def searchrec():
    if request.method == "POST":
        currsearch = request.form['searchinput']
        currsearch.lower()
        if currsearch == "" or currsearch == " ":
            return render_template("searchresult.html", search_result=[])
        currsearch = "%" + currsearch + "%"
        con = sqlite3.connect("students.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM students WHERE name like ?", (currsearch,))
            
        rows = cur.fetchall()
        
        return render_template("searchresult.html", search_result=rows)

@app.route("/delstudents", methods=["POST", "GET"])
def delstudents():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("delstudents.html", rows=rows)

@app.route("/delselection", methods=["POST", "GET"])
def delselection():
    if request.method == "POST":
        try:
            delid = request.form["delid"]
            with sqlite3.connect("students.db") as con:
                cur = con.cursor()
                
                cur.execute("DELETE FROM students WHERE user_id = ?", (delid,))
                con.commit()
                msg = "Result of removal : Record successfully removed,0"
        except:
            con.rollback()
            msg = "Result of removal : Record failed to be removed,1"
        finally:
            con.close()
            return listStudents(msg)

@app.route("/editstudents", methods=["POST", "GET"])
def editstudents():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("editstudents.html", rows=rows)

@app.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        #check if already logged in-if so send home
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        # do the standard database stuff and find the user with email
        con = sqlite3.connect("login.db")
        curs = con.cursor()
        email= request.form['email']
        curs.execute("SELECT * FROM login where email = (?)", [email])
        #return the first matching user then pass the details to
        #create a User object –unless there is nothing returned then flash a message
        row=curs.fetchone()
        if row==None:
            flash('Please try logging in again')
            return render_template('login.html')
        user = list(row)
        liUser = User(int(user[0]),user[1],user[2])
        password = request.form['password']
        match = liUser.password==password
        #if our password matches-run the login_user method
        if match and email==liUser.email:
            login_user(liUser,remember=request.form.get('remember'))
            redirect(url_for('home'))
        else:
            flash('Please try logging in again')
            return render_template('login.html')
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    cur.execute("SELECT * from login where user_id = ?" ,(user_id,))
    Liuser = cur.fetchone()
    if Liuser is None:
        return None
    else:
        return User(int(Liuser[0]), Liuser[1], Liuser[2])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)  