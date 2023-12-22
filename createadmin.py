from application import *
from application.models import *

app = create_app()
app.app_context().push()


###################
## we are using flask-migrate for create and manage database
## so instead of running any python file to create db we will use the following command
## 1. flask db init (if you already have the 'migration' directory. skip this command and go to step 2. you need to run this command only once at the beginning)
## 2. flask db migrate (you can also type some comment about what changes you have made like 'flask db migrate -m "add ip column in database"')
## 3. flask db upgrade
###################


#############################
# CREATE DEMO ADMIN
#############################
get_admin = User.query.filter_by(username='admin').first()

if not get_admin:
    role_admin = Role.query.filter_by(name='admin').first()

    if role_admin is None:
        role_admin = Role(name='admin')
        db.session.add(role_admin)
        db.session.commit()

    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    user = User(
        first_name="James",
        last_name="Gordon",
        phone='123456789', 
        username='admin', 
        email='admin@admin.com', 
        password=hashed_password, 
        role_id=role_admin.id
    )
    db.session.add(user)
    db.session.commit()

    print("Demo admin added successfully.")


#############################
# CREATE DEMO STAFF
#############################
get_staff = User.query.filter_by(username='staff').first()

if not get_staff:
    role_staff = Role.query.filter_by(name='staff').first()

    if role_staff is None:
        role_staff = Role(name='staff')
        db.session.add(role_staff)
        db.session.commit()

    hashed_password = bcrypt.generate_password_hash('staff').decode('utf-8')
    user = User(
        first_name="Alex",
        last_name="Dume",
        phone='111111111', 
        username='staff', 
        email='staff@staff.com', 
        password=hashed_password, 
        role_id=role_staff.id
    )
    db.session.add(user)
    db.session.commit()

    print("Demo staff user added successfully.")



#############################
# CREATE DEMO USER
#############################
get_user = User.query.filter_by(username='user').first()

if not get_user:
    role_user = Role.query.filter_by(name='user').first()

    if role_user is None:
        role_user = Role(name='user', default=True)
        db.session.add(role_user)
        db.session.commit()

    hashed_password = bcrypt.generate_password_hash('user').decode('utf-8')
    user = User(
        first_name="Jhone",
        last_name="Doe",
        phone='000000000', 
        username='user', 
        email='user@user.com', 
        password=hashed_password, 
        role_id=role_user.id
    )
    db.session.add(user)
    db.session.commit()

    print("Demo user added successfully.")