from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable = False)
    link = db.Column(db.String(200), nullable = False)
    screenshots = db.relationship('Screenshot', backref='project', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    message = db.Column(db.Text, nullable = False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable= False)
    password_hash = db.Column(db.String(128), nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Skill(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50), nullable = False)
    icon=db.Column(db.String(100), nullable = False)

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)



