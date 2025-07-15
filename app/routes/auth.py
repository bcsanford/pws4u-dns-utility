from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import User
from ..utils import hash_password
from sqlalchemy.exc import IntegrityError

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
