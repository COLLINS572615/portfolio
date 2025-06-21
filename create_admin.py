from app import app, db
from models import Admin

with app.app_context():
    db.create_all()  # Ensure the database and tables exist

    # Create an admin user
    admin = Admin(username='admin')
    admin.set_password('chief')  # Replace with your desired password

    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
