from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database for user storage
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        password = request.form.get('password')

        user = User.query.filter_by(gmail=gmail).first()
        if user and check_password_hash(user.password, password):
            return "Authentication Successful"  # Replace this with your logic to redirect to a dashboard
        else:
            return "Authentication Failed"  # Handle authentication failure

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        password = request.form.get('password')

        # Check if the user already exists in the database
        existing_user = User.query.filter_by(gmail=gmail).first()

        if existing_user:
            return "User already exists, please log in."  # You can customize the error message

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(gmail=gmail, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# WSGI entry point
application = app

if __name__ == '__main__':
    app.run(debug=True)

