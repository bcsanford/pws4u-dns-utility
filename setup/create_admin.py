import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from getpass import getpass

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.first():
        print("✅ Admin user already exists. Skipping creation.")
        exit(0)

    print("🛡️  No users found. Creating initial admin user.")
    while True:
        username = input("👤 Enter admin username: ").strip()
        if username:
            break
        print("❌ Username cannot be empty.")

    while True:
        password = getpass("🔑 Enter password: ")
        confirm = getpass("🔁 Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match.")
        elif not password:
            print("❌ Password cannot be empty.")
        else:
            break

    new_user = User(username=username, is_admin=True)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    print(f"✅ Admin user '{username}' created successfully.")
