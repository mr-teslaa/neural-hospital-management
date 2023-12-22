from datetime import datetime
from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import current_user
from flask_login import login_required
from application import db
from application.public.forms import BookTestForm
from application.public.forms import AppointmentForm
from application.models import User, Test, Appointment

public = Blueprint('public', __name__)

@public.route('/', methods=['GET', 'POST'])
def index():
    form = AppointmentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone = form.phone.data
            location = form.location.data

            assigned_staff = User.query.filter_by(assigned_location=location).first()

            if not assigned_staff:
                flash("No staff available in this location. Please choose a different location.", "warning")
                return redirect(url_for('users.booked_appointments'))

            appointment = Appointment(
                first_name=first_name, last_name=last_name,
                phone=phone, assigned_staff_email=assigned_staff.email,
                location=location, user_id=current_user.id
            )

            db.session.add(appointment)
            db.session.commit() 
            flash("Appoint Booked Successfully", 'success')
            return redirect(url_for('users.booked_appointments'))
        else:
            flash('You have to login first', 'success')
            return redirect(url_for('auth.login'))

    return render_template('public/index.html', form=form)

@public.route('/about/')
def about():
    return render_template('public/about.html')

@public.route('/test/book/', methods=['GET', 'POST'])
@login_required
def book_test():
    form = BookTestForm()
    # get_staff = User.query.filter_by(email='staff@staff.com').first()
    # assigned_staff = get_staff.email

    if form.validate_on_submit():
        test = Test(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            phone=form.phone.data,
            test_name=form.test_name.data,
            user_id=current_user.id
        )
        db.session.add(test)
        db.session.commit()
        flash('Test booked successfully!', 'success')
        return redirect(url_for('users.booked_tests'))
    return render_template('public/book_test.html', form=form)

@public.route('/all-tests/')
def all_tests():
    return render_template('public/all-tests.html')

@public.route('/contact/')
def contact():
    return render_template('public/contact.html')