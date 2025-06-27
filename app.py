from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from models import db, Project, Message, Admin, Skill

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'zip', 'rar', 'tar', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
    
with app.app_context():
    db.create_all()
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    profile_picture = os.path.join(app.config['UPLOAD_FOLDER'], 'profile.jpg')
    about_text = "I am a motivated and detail-oriented intermediate-level Python developer with practical experience in building web applications, chatbots, and automation scripts. I am proficient in core programming concepts, web development with Flask and Django, and database management using PostgreSQL. I am passionate about writing clean, efficient code and continuously learning new technologies. Currently, I am seeking a junior developer or internship role to contribute to meaningful projects and grow within a collaborative environment."
    return render_template('home.html', profile_picture=profile_picture, about_text = about_text)

@app.route('/about')
def about():
    skills =[
        {"name": "Python", "icon":"fab fa-python"},
        {"name": "Html", "icon":"fab fa-html5"},
        {"name": "CSS", "icon":"fab fa-css3-alt"},
        {"name": "Flask", "icon":"fas fa-flask"},
        {"name": "Django", "icon":"fas fa-server"},
        {"name": "React", "icon":"fab fa-react"},
        {"name": "SQLITE", "icon":"fas fa-database"},
        {"name": "PostgreSQL", "icon":"fas fa-database"},
        {"name": "JSON", "icon":"fas fa-database"},
        {"name": "CSV", "icon":"fas fa-database"}
    ]
    return render_template('about.html', skills=skills)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return "Thanks for the message"
    contact_details = {
        "phone" : "+254729149639",
        "email" : "collinskiprotich0@gmail.com",
        "whatsapp" : "+254729149639",
        "sms" : "Send SMS to +254729149639"
    }
    
    return render_template('contact.html', contact_details = contact_details)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        description = request.form['description']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_project = Project(title = title, description = description, link = filepath)
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('portfolio'))
    return render_template('upload.html')

@app.route('/admin/projects', methods = ['GET', 'POST'])
def admin_projects():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    # Admin logic for managing projects
    projects = Project.query.all()
    if request.method == 'POST':
        project_id = request.form['project_id']
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
    return render_template('admin_projects.html', projects=projects)

@app.route('/admin/messages', methods = ['GET', 'POST'])
def admin_messages():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    # Admin logic for managing messages
    messages = Message.query.all()
    if request.method == 'POST':
        message_id = request.form['message_id']
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/skills', methods=['GET', 'POST'])
def admin_skills():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    skills = Skill.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        icon = request.form.get('icon')
        new_skill = Skill(name=name, icon=icon)
        db.session.add(new_skill)
        db.session.commit()
        return redirect(url_for('admin_skills'))
    
    return render_template('admin_skills.html', skills=skills)

@app.route('/admin/skills/edit/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    skill = Skill.query.get_or_404(skill_id)

    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.icon = request.form.get('icon')
        db.session.commit()
        return redirect(url_for('admin_skills'))

    return render_template('edit_skill.html', skill=skill)

@app.route('/admin/skills/delete/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('admin_skills'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['is_admin'] = True
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

@app.context_processor
def inject_social_links():
    social_links = {
        "Facebook": "https://facebook.com",
        "Twitter": "https://twitter.com",
        "LinkedIn": "www.linkedin.com/in/collins-kiprotich-b82119211",
        "Instagram": "https://instagram.com",
        "GitHub": "https://github.com/COLLINS572615"
    }
    return dict(social_links=social_links)

if __name__ == '__main__':
    app.run(debug=True)
