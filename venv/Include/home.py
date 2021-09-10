from flask import Flask, render_template,request, redirect, url_for, session, abort
from flask import flash,get_flashed_messages
from datetime import datetime
import pymysql as MySQLdb
import bcrypt
import mysql.connector



app = Flask(__name__)





db= mysql.connector.connect(user='apnesh1' , password = 'Rohit123' , host = 'database-1.cbgajxq2f60f.us-east-2.rds.amazonaws.com', database = 'incogmat')
'''
class Problems(db.Model):
    
    #sno, name phone_num, msg, date, email
    
    Serial_no = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(120), nullable=False)
    image= db.Column(db.LargeBinary)
    Mobile = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    Email = db.Column(db.String(20), nullable=False)

class Contact(db.Model):
       # sno, name phone_num, msg, date, email
    
    sno = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12))
    email = db.Column(db.String(20), nullable=False)
'''


@app.route("/")
def home():
    return render_template('inc.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post", methods = ['GET', 'POST'])
def post():
    if(request.method=='POST'):
        '''Add entry to the database'''
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        ques= request.form.get('ques')
        f=request.files['img']
        entry = Problems(Mobile = mobile, Question=ques, Date= datetime.now(),Email = email ,image=f.read())
        db.session.add(entry)
        db.session.commit()

    return render_template('questions.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        msg = request.form.get('message')
        email = request.form.get('email')
        mobile = request.form.get('phone')
        entry = Contact(mobile = mobile, msg=msg, date= datetime.now(),email = email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')
@app.route("/admin" , methods = ['GET' , 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl= db.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        #print(curl)
        user=curl.fetchone()
        curl.close()
        if user == None:
            return "User Not Found!!!"
        if len(user)>0:
            if bcrypt.hashpw(password,user[1].encode('utf-8')) == user[1].encode('utf-8'):
                session['email'] = user[0]
                session['authenticate'] = True
                return redirect(url_for("dashboard"))
            else:
                return "Error password and email does not match"

    else:
        return render_template("index.html")
@app.route("/dashboard")
def dashboard():
    print(session.get("authenticate"))
    if session.get("authenticate"):
        return render_template("main.html" ,x = "I am your question!")
    return redirect(url_for("admin"))

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
      #  name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password,bcrypt.gensalt())

        cur = db.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s,%s)" , (email,hash_password))
        db.commit()
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route("/apnesh",methods=['GET','POST'])
def apnesh():
    if request.method == "GET":
        return render_template("main.html" ,x = "I am your question!")
    else:
        qid = request.form['qid']

        curl = db.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT img_txt FROM question WHERE q_id = %s",(qid,))
        x=curl.fetchone()
        curl.close()
        return render_template("main.html", x=x)


if __name__=="__main__":
    app.secret_key ='\xd9\x0f\x8c\xfb\xbf\x914"Z}L\xfcs\rG\x04\xc8"\'\x9d\xc7\xe5\x11n'
    app.run(debug=True)
