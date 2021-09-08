from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Basic database rules
class Data(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.String, default = None)
    values = db.Column('values', db.Integer)

    def __repr__(self):
        return '%s : %s'%(self.date,self.values)