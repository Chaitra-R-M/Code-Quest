from flask import Flask,request,jsonify,send_from_directory,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import enum
load_dotenv()

app=Flask(__name__,template_folder='public',static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

class Lang(enum.Enum):
    Python="Python"

db=SQLAlchemy(app)
class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(120),nullable=False)
class Progress(db.Model):
    progid = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    language =db.Column(db.Enum(Lang),nullable=True,default=None)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/python')
def pythonpage():
    return render_template('py_page.html')

@app.route('/api/register',methods=['POST'])
def register():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    if not username or not password:
        return jsonify({'message':'Username and Password required'}),400
    if User.query.filter_by(username=username).first():
        return jsonify({'message':'Username already used'}),409
    new_user=User(username=username,password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Registration complete!!'}),201

@app.route('/api/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    user=User.query.filter_by(username=username,password=password).first()
    if not user:
        return jsonify({'message':'Invalid Details!!'}),401
    return jsonify({'message':'Login Successful'}),200

@app.route('/api/language',methods=['GET'])
def addLanguage():
    data = request.get_json()
    language=data.get('language')
    if language =="Python":
        return jsonify({'message':'Enjoy learning Python'})
    

if __name__=='__main__':
    app.run(debug=True,port=5050)