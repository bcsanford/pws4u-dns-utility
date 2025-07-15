# app/routes/admin.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User
from app import db, bcrypt

admin_bp = Blueprint("admin", __name__)

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template("admin.html", users=users)

@admin_bp.route("/admin/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for("admin.admin_dashboard"))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/reset_password/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password")
    if not new_password:
        flash("Password cannot be empty.", "danger")
        return redirect(url_for("admin.admin_dashboard"))
    user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()
    flash(f"Password for '{user.username}' has been reset.", "success")
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/set_role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def set_role(user_id):
    user = User.query.get_or_404(user_id)
    role = request.form.get("role")
    if role not in ["admin", "user"]:
        flash("Invalid role.", "danger")
        return redirect(url_for("admin.admin_dashboard"))
    user.is_admin = True if role == "admin" else False
    db.session.commit()
    flash(f"Role for '{user.username}' set to '{role}'.", "success")
    return redirect(url_for("admin.admin_dashboard"))
