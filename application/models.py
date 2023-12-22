# from sqlalchemy.dialects.sqlite import UUID
from datetime import datetime
from flask import current_app

#   importing dataase
from application import db

#   importing login manager
from application import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    profile = db.Column(db.String(500), nullable=False, default='defaultavatar.jpg')
    password = db.Column(db.String(500), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip = db.Column(db.String(100))
    last_ip = db.Column(db.String(100))
    assigned_location = db.Column(db.String(100))
    appointments = db.relationship('Appointment', backref='patients', lazy=True)
    tests = db.relationship('Test', backref='patients', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role", backref='user_roles')

    def has_role(self, role):
        return self.role.name == role



class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.String(100))
    users = db.relationship('User', back_populates='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = ''
            
    def add_permission(self, permission):
        if permission not in self.permissions.split(','):
            self.permissions = f"{self.permissions},{permission}"
    
    def remove_permission(self, permission):
        if permission in self.permissions.split(','):
            self.permissions = self.permissions.replace(f"{permission},", '')
            
    def has_permission(self, permission):
        return permission in self.permissions.split(',')
    
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), default='pending')
    prescription = db.Column(db.String(999), default='defaultreport.jpg')
    appointment_date = db.Column(db.DateTime)
    assigned_staff_email = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    test_name = db.Column(db.String(150))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    status = db.Column(db.String(100), default='pending')
    report = db.Column(db.String(999), nullable=False, default='defaultreport.jpg')
    appointment_date = db.Column(db.DateTime)
    assigned_staff_email = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    