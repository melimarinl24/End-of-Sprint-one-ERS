from flask_login import UserMixin
from project import db

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # Student-only
    nshe_id = db.Column(db.String(10), nullable=True)

    # Faculty-only
    employee_id = db.Column(db.String(15), nullable=True)

    # NEW
    password_hash = db.Column(db.String(255), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)
    role = db.relationship('Role', backref='users', lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'), nullable=True)  # will fix this next
    major_id = db.Column(db.Integer, db.ForeignKey('Majors.id'), nullable=True)  # faculty won't have this

class Role(db.Model):
    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Department(db.Model):
    __tablename__ = 'Departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Major(db.Model):
    __tablename__ = 'Majors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'), nullable=False)

