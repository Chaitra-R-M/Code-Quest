from flask import Flask,request,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(120),nullable=False)

with app.app_context():
    db.create_all()

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
    return jsonify({'message':'Login successful!!'}),200

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public',path)
if __name__=='__main__':
    app.run(debug=True)