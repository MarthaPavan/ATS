from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    resume_file = db.Column(db.String(300))
    raw_text = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name or 'Not Mentioned',
            'email': self.email or 'Not Mentioned',
            'education': self.education or 'Not Mentioned',
            'skills': self.skills or 'Not Mentioned',
            'experience': self.experience or 'Not Mentioned',
            'resume_file': self.resume_file or ''
        }
