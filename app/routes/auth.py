from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from ..utils import verify_password, hash_password
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and verify_password(password, user.password_hash):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Only allow access if the current user is admin
    if not current_user.is_admin:
        flash("Unauthorized access. Admins only.", "danger")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        discord_username = request.form.get('discord_username').strip() or None
        is_admin = bool(request.form.get('is_admin'))

        if not username or not password:
            return render_template("register.html", error="Username and password are required.")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already exists.")

        try:
            new_user = User(
                username=username,
                password_hash=hash_password(password),
                discord_username=discord_username,
                is_admin=is_admin
            )
            db.session.add(new_user)
            db.session.commit()
            return render_template("register.html", success=f"User '{username}' created successfully.")
        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="Failed to create user due to database error.")

    return render_template("register.html")
