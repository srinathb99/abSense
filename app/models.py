from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return StudentUser.query.get(int(id)) or FacultyUser.query.get(int(id))

class StudentUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class FacultyUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class leaves(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_username = db.Column(db.String(64), index = True, unique = False)
    faculty_username = db.Column(db.String(64), index = True, unique = False)
    from_date = db.Column(db.DateTime, index = True, unique = False)
    to_date = db.Column(db.DateTime, index = True, unique = False)
    reason = db.Column(db.String(64), index = True, unique = False)
    type_of_leave = db.Column(db.String(64), index = True, unique = False)
    leave_status = db.Column(db.String(20), index = True, unique = False)
