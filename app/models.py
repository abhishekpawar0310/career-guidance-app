from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    education_level = db.Column(db.String(10))  # '10th' or '12th'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship('AssessmentResult', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)      # '10th' or '12th'
    text = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(20), nullable=False)   # 'interest' or 'aptitude'
    order = db.Column(db.Integer, default=0)

    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    trait_scores = db.Column(db.JSON, nullable=False)     # e.g. {"R":1,"I":0,"A":0,"S":0,"E":0,"C":0}


class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    riasec_profile = db.Column(db.JSON)       # e.g. {"R":2,"I":8,"A":1,"S":3,"E":5,"C":4}
    aptitude_profile = db.Column(db.JSON)     # e.g. {"logical":8,"verbal":4,"numerical":6}
    suited_level = db.Column(db.String(10))   # '10th', '12th', or 'both'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    career = db.relationship('Career', backref='courses')


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    contact = db.Column(db.String(100))
    website = db.Column(db.String(200))


class CollegeCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    fees = db.Column(db.String(100))
    apply_link = db.Column(db.String(300))

    college = db.relationship('College', backref='offerings')
    course = db.relationship('Course', backref='offerings')


class AssessmentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.String(10))
    riasec_scores = db.Column(db.JSON)
    aptitude_scores = db.Column(db.JSON)
    recommended_careers = db.Column(db.JSON)   # list of {career_id, name, match_percent}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)