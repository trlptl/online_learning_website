from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

# User Model
class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(100), nullable=False)


# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text, nullable=True)
    course_duration = db.Column(db.String(100), nullable=False)
    course_author_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
