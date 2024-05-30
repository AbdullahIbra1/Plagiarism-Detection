# db.py
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def setup_db(app):
	db.app = app
	db.init_app(app)

class Text(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(), nullable=False)

class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), nullable=False,unique=True)
	password = db.Column(db.String(120), nullable=False)
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(120), nullable=False)

	def set_password(self, password):
		self.password = password
	def check_password(self, password):
		return self.password==password

def add_user(username, password):
	user = User(username=username)
	user.set_password(password)
	db.session.add(user)
	db.session.commit()

def add_text(text):
	newtext=Text(content=text)
	db.session.add(newtext)
	db.session.commit()
