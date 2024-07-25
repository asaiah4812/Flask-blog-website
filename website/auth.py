from flask import Blueprint, render_template, url_for, request, redirect
from . import db
from .models import User
from flask import flash
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login successfull 🙌", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect.", category='warning')
        else:
            flash('Email does not exist.', category="error")
  
    return render_template('auth/login.html', user=current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use', category="error") 
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(username) < 5:
            flash('Username most be more than 5 letters', category='error')
        elif len(password1) < 6:
            flash('Password most be more than 6 letters', category='error')
        elif len(email) < 10:
            flash("Email is Invalid", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfull login to continue', category='success')
            return redirect(url_for('auth.login'))
             
             

    return render_template("auth/signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

