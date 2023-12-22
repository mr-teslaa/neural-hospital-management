import os
from flask import render_template, Blueprint, request, jsonify, current_app, flash, send_file, redirect, url_for
from flask_login import login_required, current_user
from application import db
from application.models import User, Role, Appointment, Test
from application.utils.AdminCustomAuth import staff_required
from sqlalchemy import not_

staffs = Blueprint('staffs', __name__)

@staffs.route('/dashboard/')
@login_required
@staff_required
def staff_dashboard():
    completed_appointments = Appointment.query.filter(
        Appointment.status == 'completed',Appointment.assigned_staff_email == current_user.email
    ).all()
    pending_appointments = Appointment.query.filter(
        not_(Appointment.status == 'completed'),Appointment.assigned_staff_email == current_user.email
    ).all()
    completed_tests = Test.query.filter(
        Test.status == 'completed',Appointment.assigned_staff_email == current_user.email
    ).all()
    pending_tests = Test.query.filter(
        not_(Test.status == 'completed'),Appointment.assigned_staff_email == current_user.email
    ).all()
    return render_template(
        "staffs/staff_dashboard.html", title="Staff Dashboard",
        completed_appointments=completed_appointments, pending_appointments=pending_appointments,
        completed_tests=completed_tests, pending_tests=pending_tests,
        appointments=appointments, tests=tests        
    )


#####################################
## APPOINTMENTS
#####################################
@staffs.route('/dashboard/appointments/')
@login_required
@staff_required
def appointments():
    current_staff = User.query.filter_by(email=current_user.email).first()

    appointments = Appointment.query.filter(
        not_(Appointment.status == 'completed'),Appointment.assigned_staff_email == current_staff.email
    ).all()
    return render_template("staffs/appointments.html", appointments=appointments)

@staffs.route('/dashboard/appointment/status/<int:appointment_id>/', methods=['POST'])
@login_required
@staff_required
def update_appointment_status(appointment_id):
    # Getting the new status from the form
    new_status = request.json['status']
    appointment = Appointment.query.get(appointment_id)

    # Checking if the form data is valid
    valid_statuses = ['pending-date', 'pending-test', 'pending-report', 'completed']
    if appointment and new_status in valid_statuses:
        appointment.status = new_status
        db.session.commit()
        return jsonify({'message': 'Appointment status updated successfully'}), 200
    else:
        return jsonify({'message': 'Appointment not found or something went wrong'}), 404
#####################################
## TESTS
#####################################
@staffs.route('/dashboard/tests/')
@login_required
@staff_required
def tests():
    tests = Test.query.filter_by(assigned_staff_email=current_user.email).all()
    return render_template("staffs/tests.html", tests=tests)


@staffs.route('/dashboard/test/booked/<int:test_id>/download_report/', methods=['POST'])
@login_required
@staff_required
def download_test(test_id):
    test = Test.query.get_or_404(test_id)
    
    if test.report:
        report_path = os.path.join(current_app.root_path, 'static/uploads/reports', test.report)
        
        if os.path.exists(report_path):
            return send_file(report_path, as_attachment=True)
        else:
            flash('Report file not found.', 'danger')
        
    else:
        flash('No report available for download.', 'warning')
    
    return redirect(url_for('staffs.tests'))