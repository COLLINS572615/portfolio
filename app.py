from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import db, Project, Message

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'zip', 'rar', 'tar'}


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
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return "Thanks for the message"
    return render_template('contact.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == "POST":
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
    messages = Message.query.all()
    if request.method == 'POST':
        message_id = request.form['message_id']
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
    return render_template('admin_messages.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
