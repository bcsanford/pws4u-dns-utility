from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed, is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("register.html", form=form)
