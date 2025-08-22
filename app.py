import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Resume
from parser_utils import parse_resume
from search_utils import search
import pandas as pd
from io import StringIO

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('Provide username and password', 'danger')
            return redirect(url_for('signup'))
        if User.query.filter_by(username=username).first():
            flash('Username exists', 'warning')
            return redirect(url_for('signup'))
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'resume' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(save_path)
        parsed = parse_resume(save_path)
        resume = Resume(
            name=parsed.get('name'),
            email=parsed.get('email'),
            education=parsed.get('education'),
            skills=parsed.get('skills'),
            experience=parsed.get('experience'),
            resume_file=filename,
            raw_text=parsed.get('raw_text')
        )
        db.session.add(resume)
        db.session.commit()
        flash('Resume uploaded and parsed successfully', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('File type not allowed', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET','POST'])
@login_required
def search_view():
    results = None
    query = {'skills':'', 'education':''}
    if request.method == 'POST':
        skills = request.form.get('skills','')
        education = request.form.get('education','')
        results = search(db.session, skills=skills, education=education)
        query = {'skills':skills, 'education':education}
    return render_template('search.html', results=results, query=query)

@app.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    skills = request.form.get('skills_hidden','')
    education = request.form.get('education_hidden','')
    results = search(db.session, skills=skills, education=education)
    rows = [r.to_dict() for r in results]
    if not rows:
        flash('No matching profiles to export', 'warning')
        return redirect(url_for('search_view'))
    df = pd.DataFrame(rows)
    csv_io = StringIO()
    df.to_csv(csv_io, index=False)
    csv_io.seek(0)
    response = make_response(csv_io.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=search_results.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/results')
@login_required
def results_page():
    candidates = Resume.query.all()
    return render_template('results.html', candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True)
