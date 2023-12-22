import os
from flask import current_app, render_template, send_file, Blueprint, flash, redirect, url_for
from flask_login import current_user
from flask_login import login_required
from application.models import Appointment
from application.models import Test
from application.utils.AdminCustomAuth import user_required

users = Blueprint('users', __name__)

################################
# USER DASHBOARD
################################
@users.route('/dashboard/')
@login_required
@user_required
def user_dashboard():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    tests = Test.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "users/user_dashboard.html", title="Dashboard",
        appointments=appointments, tests=tests
    )

################################
# ALL APPOINTMENTS
################################
@users.route('/dashboard/appointments/booked/')
@login_required
@user_required
def booked_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "users/booked_appointments.html", 
        appointments=appointments,
        title="Booked Appointment"
    )

################################
# DOWNLOAD PRESCRIPTION 
################################
@users.route('/dashboard/appointment/booked/<int:appointment_id>/prescription/download/', methods=['POST'])
@login_required
@user_required
def download_prescription(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.prescription:
        if appointment.patients == current_user:  # Validate that only the associated user can download
            report_path = os.path.join(current_app.root_path, 'static/uploads/prescriptions', appointment.prescription)
            
            if os.path.exists(report_path):
                return send_file(report_path, as_attachment=True)
            else:
                flash('Prescription file not found.', 'danger')
        else:   
            flash('No prescription found', 'danger')
    else:
        flash('No prescription available for download.', 'warning')
    
    return redirect(url_for('users.booked_appointments'))


################################
# ALL BOOKED TEST
################################
@users.route('/dashboard/tests/booked/')
@login_required
@user_required
def booked_tests():
    tests = Test.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "users/booked_tests.html", 
        tests=tests,
        title="Booked Tests"
    )


################################
# DOWNLOAD TEST REPORT
################################
@users.route('/dashboard/test/booked/<int:test_id>/report/download/', methods=['POST'])
@login_required
@user_required
def download_test(test_id):
    test = Test.query.get_or_404(test_id)
    
    if test.report:
        if test.patients == current_user:  # Validate that only the associated user can download
            report_path = os.path.join(current_app.root_path, 'static/uploads/reports', test.report)
            
            if os.path.exists(report_path):
                return send_file(report_path, as_attachment=True)
            else:
                flash('Report file not found.', 'danger')
        else:   
            flash('No report found', 'danger')
    else:
        flash('No report available for download.', 'warning')
    
    return redirect(url_for('users.booked_tests', test_id=test_id))