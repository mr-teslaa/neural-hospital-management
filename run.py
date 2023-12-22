from application import create_app, db

app = create_app()

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# from flask import Flask, render_template
# from models import db
# from views.adminViews import admin_bp
# from views.userViews import user_bp
# from views.staffViews import staff_bp


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.secret_key="neuroglobal"
# db.init_app(app)

# app.register_blueprint(admin_bp, url_prefix='/admin')
# app.register_blueprint(user_bp, url_prefix='/user')
# app.register_blueprint(staff_bp, url_prefix='/staff')

# # ... define the User model and other routes ...
# @app.route("/")
# def homepage():
#     return render_template('index.html')

# @app.route("/about")
# def about():
#     return render_template('about.html')

# @app.route("/tests")
# def test():
#     return render_template('service.html')

# @app.route("/contact")
# def contact():
#     return render_template('contact.html')


# if __name__ == '__main__':
#     with app.app_context():
#         # Create the database and tables
#         db.create_all()


#     app.run(debug=True)
