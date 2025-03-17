from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    Fullname = db.Column(db.String(100), nullable=False)
    Qualification = db.Column(db.String(100), nullable=False)
    DOB = db.Column(db.Date , nullable=False)
    
    scores = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Admin(id={self.id}, username={self.username})>"

class Subject(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

    def __repr__(self):
        return f"<Chapter(id={self.id}, name={self.name})>"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.Date , nullable=False)
    duration = db.Column(db.Interval , nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"<Quiz(id={self.id}, title={self.title})>"

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Question(id={self.id}, question={self.question})>"

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Score(id={self.id}, score={self.score})>"
