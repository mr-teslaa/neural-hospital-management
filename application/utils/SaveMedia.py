#   importing necessary module
import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app

#   SAVE REPORT
def save_report(file, test):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    report_fn = f"report-{test.patients.username}-{random_hex}-neuroglobal{f_ext}"
    report_path = os.path.join(current_app.root_path, 'static/uploads/reports', report_fn)

    if f_ext.lower() == '.pdf':
        file.save(report_path)
    elif f_ext.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
        output_size = (300, 300)    
        i = Image.open(file)
        i.thumbnail(output_size)
        i.save(report_path)
    else:
        raise ValueError("Unsupported file format")

    return report_fn


#   SAVE PERSCRIPTION
def save_prescription(file, appointment):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    report_fn = f"prescription-{appointment.first_name}-{random_hex}-neuroglobal{f_ext}"
    report_path = os.path.join(current_app.root_path, 'static/uploads/prescriptions', report_fn)

    if f_ext.lower() == '.pdf':
        file.save(report_path)
    elif f_ext.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
        output_size = (300, 300)    
        i = Image.open(file)
        i.thumbnail(output_size)
        i.save(report_path)
    else:
        raise ValueError("Unsupported file format")

    return report_fn