import os
import json

from datetime import datetime

#   importing basic flask module
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import abort
from flask import jsonify
from flask import make_response
from flask import current_app

#   importing module from flask login
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from application import db
from application import bcrypt

from application.models import User
from application.models import Role

from application.auth.forms import RegistrationForm
from application.auth.forms import LoginForm

from application.utils.Generate import generate_username

auth = Blueprint('auth', __name__)

@auth.route('/register/', methods=['GET','POST'])
def register():
    current_ip = request.remote_addr

    if current_user.is_authenticated: 
        if current_user.has_role('admin'):
            return redirect(url_for('admin.admin_dashboard'))
    
        return redirect(url_for('users.user_dashboard'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        # create the staff role if it doesn't exist
        role_user = Role.query.filter_by(name='user').first()

        if role_user is None:
            role_user = Role(name='user')
            db.session.add(role_user)
            db.session.commit()

        hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
        username = generate_username(form.first_name.data.strip(), form.last_name.data.strip())

        user = User(
            first_name=form.first_name.data.strip(), 
            last_name=form.last_name.data.strip(), 
            username=username,
            email=form.email.data, 
            phone=form.phone.data, 
            password=hashed_password, 
            role_id=role_user.id,
            ip=current_ip
        )
        db.session.add(user)
        db.session.commit()
        # log the ip
        current_user.last_ip = current_ip
        db.session.commit()
        
        flash('Registration Complete, you can now login', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('auth/register.html', form=form)


#  USER LOGIN
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    current_ip = request.remote_addr

    if current_user.is_authenticated:
        # log the ip
        current_user.last_ip = current_ip
        db.session.commit()

        if current_user.has_role('admin'):
            return redirect(url_for('admin.admin_dashboard'))
    
        if current_user.has_role('staff'):
            return redirect(url_for('staffs.staff_dashboard'))
    
        if current_user.has_role('user'):
            return redirect(url_for('users.user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data.strip()):
            # check if the user is an admin
            if user.role.name == 'admin':
                login_user(user, remember=form.remember.data)
                flash('You have been logged in as admin', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role.name == 'staff':
                login_user(user, remember=form.remember.data)
                flash('You have been logged in as staff', 'success')
                return redirect(url_for('staffs.staff_dashboard'))
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login success', 'success')
                return redirect(next_page) if next_page else redirect(url_for('users.user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html', form=form, title='Login')


#   LOGOUT
@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

