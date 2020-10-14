from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/incogmaths'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Problems(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    Serial_no = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(120), nullable=False)
    image= db.Column(db.LargeBinary)
    Mobile = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    Email = db.Column(db.String(20), nullable=False)

class Contact(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12))
    email = db.Column(db.String(20), nullable=False)



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

app.run(debug=True)
