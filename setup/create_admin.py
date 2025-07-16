import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))import os
import getpass
from app import create_app, db
from app.models import User

app = create_app()

def create_admin_user():
    with app.app_context():
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print("✅ Admin user already exists. Exiting.")
            return

        print("👤 Create Initial Admin User")
        while True:
            username = input("🆔 Username: ").strip()
            if not username:
                print("⚠️ Username cannot be empty.")
                continue
            if User.query.filter_by(username=username).first():
                print("⚠️ Username already exists.")
                continue
            break

        while True:
            password = getpass.getpass("🔑 Password: ")
            confirm = getpass.getpass("🔁 Confirm Password: ")
            if not password or password != confirm:
                print("⚠️ Passwords do not match or are empty.")
                continue
            break

        user = User(username=username, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Admin user '{username}' created successfully.")

if __name__ == "__main__":
    create_admin_user()
