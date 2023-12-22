from datetime import datetime, timedelta
from flask import render_template, Blueprint, redirect, url_for, flash, request, session, jsonify
from sqlalchemy import and_, not_, func
from flask_login import login_required
from application import db, bcrypt
from application.models import User, Test, Role, Appointment
from application.admin.forms import NewUserForm, NewStaffForm, EditStaffForm, EditBookedTestForm, EditAppointmentsForm
from application.utils.AdminCustomAuth import admin_required
from application.utils.Generate import generate_username
from application.utils.SaveMedia import save_report, save_prescription

admin = Blueprint('admin', __name__)

################################
# ADMIN DASHBOARD
################################
@admin.route('/dashboard/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_dashboard():
    today = datetime.now().date()  # Get today's date
    appointments = Appointment.query.all()
    tests = Test.query.all()
    pending_tests = Test.query.filter(not_(Test.status=='completed')).all()

    # Query upcoming appointments for the current user
    upcomming_appointments = Appointment.query.filter(Appointment.appointment_date > today).all()
    return render_template(
        'admin/dashboard.html', title="Admin Dashboard",                     
        appointments=appointments, tests=tests, pending_tests=pending_tests,
        upcomming_appointments=upcomming_appointments
    )

############################################
# APPOINTMENT CHART DATA - ADMIN DASHBOARD
###########################################
@admin.route('/dashboard/booking-chart-data')
@login_required
@admin_required
def booking_chart_data():
    today = datetime.now().date()
    end_date = today + timedelta(days=15)

    print(f'today: {today}')
    print(f'end date: {end_date}')

    appointment_query = Appointment.query.filter(
        Appointment.appointment_date >= today,
        Appointment.appointment_date <= end_date
    )

    
    test_query = Test.query.filter(
        Test.appointment_date >= today,
        Test.appointment_date <= end_date
    )

    appointments = appointment_query.all()
    tests = test_query.all()
    print(appointments)

    appointment_counts = {}
    for appointment in appointments:
        date = appointment.appointment_date.date().strftime('%Y-%m-%d')
        if date in appointment_counts:
            appointment_counts[date] += 1
        else:
            appointment_counts[date] = 1

    test_counts = {}
    for test in tests:
        date = test.appointment_date.date().strftime('%Y-%m-%d')
        if date in test_counts:
            test_counts[date] += 1
        else:
            test_counts[date] = 1

    labels = list(appointment_counts.keys())
    appointment_data = [appointment_counts[label] for label in labels]
    test_data = [test_counts.get(label, 0) for label in labels]

    return jsonify({
        'labels': labels,
        'appointments': appointment_data,
        'tests': test_data
    })

################################
# APPOINTMENTS
################################
@admin.route('/dashboard/appointments/booked/')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.all()
    return render_template(
        "admin/appointments.html", 
        appointments=appointments,
        title="Booked Appointments"
    )

################################
# EDIT APPOINTMENT
################################
@admin.route('/dashboard/appointment/booked/<int:appointment_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    form = EditAppointmentsForm()

    if form.validate_on_submit():
        if form.first_name.data and form.first_name.data != appointment.first_name:
            appointment.first_name = form.first_name.data
        
        if form.last_name.data and form.last_name.data != appointment.last_name:
            appointment.last_name = form.last_name.data

        if form.phone.data and form.phone.data != appointment.phone:
            appointment.phone = form.phone.data

        if form.location.data and form.location.data != appointment.location:
            appointment.location = form.location.data

        if form.prescription.data:
            picture_file = save_prescription(form.prescription.data, appointment=appointment)
            print('we have prescription in form and the path is: {picture_file}')
            appointment.prescription = picture_file
 
        print('finally prescription path is {appointment.prescription}')
        db.session.commit()
        flash('Appointment updated successfully', 'success')
        return redirect(url_for('admin.appointments'))    

    if request.method == 'GET':
        form.first_name.data = appointment.first_name
        form.last_name.data = appointment.last_name
        form.phone.data = appointment.phone
    return render_template(
        "admin/edit_appointment.html", 
        appointments=appointments, form=form,
        title="Booked Appointments"
    )

################################
# UPDATE STATUS APPOINTMENT
################################
@admin.route('/dashboard/appointment/status/<int:appointment_id>/', methods=['POST'])
@login_required
@admin_required
def update_appointment_status(appointment_id):
    # Getting the new status from the form
    new_status = request.json['status']
    appointment = Appointment.query.get(appointment_id)

    # Checking if the form data is valid
    valid_statuses = ['pending-date', 'pending-test', 'pending-report', 'completed']
    if appointment and new_status in valid_statuses:
        appointment.status = new_status
        db.session.commit()
        flash('Appointment status updated successfully', 'success')
        return jsonify({'message': 'Appointment status updated successfully'}), 200
    else:
        flash('Appointment not found or something went wrong', 'success')
        return jsonify({'message': 'Appointment not found or something went wrong'}), 404
    

################################
# UPDATE DATE APPOINTMENT
################################
@admin.route('/dashboard/appointment/date/<int:appointment_id>/', methods=['POST'])
@login_required
@admin_required
def update_appointment_date(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    get_new_date = request.json.get('date')

    try:
        new_date = datetime.strptime(get_new_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    appointment.appointment_date = new_date
    db.session.commit()

    flash('Appointment Date Updated', 'success')
    return jsonify({'message': 'Appointment date updated successfully'}), 200

################################
# ALL BOOKED TEST
################################
@admin.route('/dashboard/tests/booked/')
@login_required
@admin_required
def tests():
    tests = Test.query.all()
    return render_template(
        "admin/tests.html", 
        tests=tests,
        title="Booked Tests"
    )

################################
# EDIT OR VIEW A TEST
################################
@admin.route('/dashboard/test/booked/<int:test_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def view_test(test_id):
    form = EditBookedTestForm()
    test = Test.query.get_or_404(test_id)

    if form.validate_on_submit():
        if form.email.data and form.email.data != test.email:
            test.email = form.email.data

        if form.phone.data and form.phone.data != test.phone:
            test.phone = form.phone.data

        if form.test_name.data and form.test_name.data != test.test_name:
            test.test_name = form.test_name.data

        if form.appointment_date.data and form.appointment_date.data != test.appointment_date:
            test.appointment_date = form.appointment_date.data

        # if form.report.data and form.report.data != test.patients.report:
            # test.patients.report = form.report.data

        if form.report.data:
            picture_file = save_report(form.report.data, test=test)
            test.report = picture_file
            # imagefile = url_for('static', filename='productimages/' + picture_file)
 
        db.session.commit()
        return redirect(url_for('admin.tests'))    

    if request.method == 'GET':
        form.patient_name.data = f'{test.patients.first_name} {test.patients.last_name}'
        form.email.data = test.patients.email
        form.phone.data = test.patients.phone


    return render_template(
        "admin/view_test.html", 
        test=test, form=form,
        title="View Booked Test"
    )

################################
# ALL USERS
################################
@admin.route('/dashboard/users/', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    users = User.query.filter_by(role_id=Role.query.filter_by(name='user').first().id).all()
    return render_template('admin/users.html', users=users)

################################
# ADD NEW USER
################################
@admin.route('/dashboard/user/new/', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    form = NewUserForm()

    if form.validate_on_submit():
        # create the staff role if it doesn't exist
        role_staff = Role.query.filter_by(name='user').first()

        hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
        username = generate_username(form.first_name.data.strip(), form.last_name.data.strip())

        user = User(
            first_name=form.first_name.data.strip(), 
            last_name=form.last_name.data.strip(), 
            phone=form.phone.data,
            username=username,
            email=form.email.data, 
            password=hashed_password, 
            role_id=role_staff.id
        )
        db.session.add(user)
        db.session.commit()
        
        flash('New User Added', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/new_user.html', form=form)

################################
# EDIT USER PROFILE
################################
@admin.route('/dashboard/user/edit/<string:username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(username):
    get_user = User.query.filter_by(username=username).first()

    if get_user and get_user.has_role('user'):
        form = EditStaffForm()

        if form.validate_on_submit():
             # Get form data
            new_password = form.password.data
            confirm_new_password = form.confirm_password.data
            
            if new_password != confirm_new_password:
                flash('New Password and Confirm Password Doesn\'t Matched ⚠️', 'danger')
                return redirect(url_for('admin.user_edit', username=get_user.username))
        
            if new_password and confirm_new_password and new_password==confirm_new_password:
                hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
                get_user.password=hashed_password

            if get_user.first_name != form.first_name.data:
                get_user.first_name = form.first_name.data.strip()

            if get_user.last_name != form.last_name.data:
                get_user.last_name=form.last_name.data.strip() 
            
            if get_user.phone != form.phone.data:
                get_user.phone=form.phone.data
            
            if get_user.email != form.email.data:
                get_user.email=form.email.data
            
            db.session.commit()
            
            flash('User Porfile Updated', 'success')
            return redirect(url_for('admin.users'))

        if request.method == 'GET':
            form.first_name.data=get_user.first_name
            form.last_name.data=get_user.last_name
            form.phone.data=get_user.phone
            form.email.data=get_user.email
    
    else:
        flash('Invalid staff account', 'danger')
    return render_template('admin/new_user.html', form=form)

################################
# ALL STAFFS
################################
@admin.route('/dashboard/staffs/', methods=['GET', 'POST'])
@login_required
@admin_required
def staffs():
    staffs = User.query.filter_by(role_id=Role.query.filter_by(name='staff').first().id).all()
    return render_template('admin/staffs.html', staffs=staffs)

################################
# ADD NEW STAFF
################################
@admin.route('/dashboard/staff/new/', methods=['GET', 'POST'])
@login_required
@admin_required
def new_staff():
    form = NewStaffForm()

    if form.validate_on_submit():
        # create the staff role if it doesn't exist
        role_staff = Role.query.filter_by(name='staff').first()

        hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
        username = generate_username(form.first_name.data.strip(), form.last_name.data.strip())

        staff = User(
            first_name=form.first_name.data.strip(), 
            last_name=form.last_name.data.strip(), 
            phone=form.phone.data,
            username=username,
            email=form.email.data, 
            password=hashed_password,
            assigned_location = form.assigned_location.data, 
            role_id=role_staff.id
        )
        db.session.add(staff)
        db.session.commit()
        
        flash('New Staff Added', 'success')
        return redirect(url_for('admin.staffs'))
    return render_template('admin/new_staff.html', form=form)

################################
# EDIT STAFF PROFILE
################################
@admin.route('/dashboard/staff/edit/<string:username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def staff_edit(username):
    get_staff = User.query.filter_by(username=username).first()

    if get_staff and get_staff.has_role('staff'):
        form = EditStaffForm()

        if form.validate_on_submit():
             # Get form data
            new_password = form.password.data
            confirm_new_password = form.confirm_password.data
            
            if new_password != confirm_new_password:
                flash('New Password and Confirm Password Doesn\'t Matched ⚠️', 'danger')
                return redirect(url_for('admin.staff_edit', username=get_staff.username))
        
            if new_password and confirm_new_password and new_password==confirm_new_password:
                hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
                get_staff.password=hashed_password

            if get_staff.first_name != form.first_name.data:
                get_staff.first_name = form.first_name.data.strip()

            if get_staff.last_name != form.last_name.data:
                get_staff.last_name=form.last_name.data.strip() 
            
            if get_staff.phone != form.phone.data:
                get_staff.phone=form.phone.data
            
            if get_staff.email != form.email.data:
                get_staff.email=form.email.data
            
            if get_staff.assigned_location != form.assigned_location.data:
                get_staff.assigned_location=form.assigned_location.data

            db.session.commit()
            
            flash('Staff Porfile Updated', 'success')
            return redirect(url_for('admin.staffs'))

        if request.method == 'GET':
            form.first_name.data=get_staff.first_name
            form.last_name.data=get_staff.last_name
            form.phone.data=get_staff.phone
            form.email.data=get_staff.email
    
    else:
        flash('Invalid staff account', 'danger')
    return render_template('admin/new_staff.html', form=form)

################################
# UPDATE STAFF LOCATION 
################################
@admin.route('/dashboard/staff/<string:staff_username>/location/update/', methods=['POST'])
@login_required
@admin_required
def update_staff_location(staff_username):
    new_location = request.form.get('assignedLocation')
    get_staff_username = staff_username

    # Update the appointment status in the database for the specific appointment
    get_staff = User.query.filter_by(username=get_staff_username).first()
    print(f'get staff: {get_staff.email}')  
    if get_staff and new_location == 'kolkata-airport-area' or new_location == 'habra' or new_location == 'bongaon':
        get_staff.assigned_location = new_location
        db.session.commit()

        if get_staff.assigned_location == 'kolkata-airport-area':
            new_assigned_location = 'Kolkata Airport Area'

        if get_staff.assigned_location == 'habra':
            new_assigned_location = 'Habra'
            
        if get_staff.assigned_location == 'bongaon':
            new_assigned_location = 'Bongaon'

        flash('Location assigned successfully', 'success')
        return redirect(url_for('admin.staffs'))
    else:
        flash('Could not find the staff or invalid location', 'danger')
        return redirect(url_for('admin.staffs'))

################################
# DELETE STAFF
################################
@admin.route('/dashboard/staff/delete/<string:username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def staff_delete(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash(f'Staff "{user.first_name} {user.last_name}" Deleted ✅', 'success')
    return redirect(url_for('admin.staffs'))