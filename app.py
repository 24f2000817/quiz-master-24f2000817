
from flask import Flask, render_template
from controllers.database import *
from controllers.config import config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()

    user_admin = User.query.filter_by(user_email = "admin@gmail.com").first()
    if not user_admin:
        user_admin = User(
            username = "admin",
            user_email = "admin@gmail.com",
            password = "123456789",
            qualification = "MCA",
            dob = datetime.strptime("2000-01-01", "%Y-%m-%d"),
            role = "admin"
        )
        db.session.add(user_admin)
    db.session.commit()

# I am creating sample data for testing purposes as when I make changes in database all the data will be deleted
# so I am creating sample data here only for my reference, This will not be added in production
    user_user = User.query.filter_by(user_email = "user1@gmail.com").first()
    if not user_user:
        user_user = User(
            username = "user1",
            user_email = "user1@gmail.com",
            password = "user1123",
            qualification = "PUC",
            dob = datetime.strptime("2009-01-01", "%Y-%m-%d"),
            role = "user"
        )
        db.session.add(user_user)
    db.session.commit()

    subject = Subject.query.filter_by(name = "Physics").first()
    if not subject:
        subject = Subject(
            name = "Physics",
            description = "Physics is a natural science that studies matter, its motion and behavior through space and time, and the related entities of energy and force."
        )
        db.session.add(subject)
    db.session.commit()

    chapter = Chapter.query.filter_by(name = "Units and Measurement").first()
    if not chapter:
        chapter = Chapter(
            name = "Units and Measurement",
            subject_id = 1,
            description = "Units and Measurement is a fundamental part of physics that deals with the measurement of physical quantities, such as length, mass, time, and temperature."
        )
        db.session.add(chapter)
    db.session.commit()

    quiz = Quiz.query.filter_by(chapter_id = 1).first()
    if not quiz:
        quiz = Quiz(
            chapter_id = 1,
            date_of_quiz = datetime.strptime("2025-04-01", "%Y-%m-%d"),
            duration = 60,
            remarks = "This is a sample quiz"
        )
        db.session.add(quiz)
    db.session.commit()

    question = Question.query.filter_by(quiz_id = 1).first()
    if not question:
        question = Question(
            quiz_id = 1,    
            question_title = "SI Unit",
            question_statement = "What is the SI unit of force?",
            option1 = "Newton",
            option2 = "Meter",
            option3 = "Second",
            option4 = "Ampere",
            correct_option = "Newton"
        )
        db.session.add(question)
    db.session.commit()

from controllers.authentication import *
from controllers.routes import *
from controllers.edit_routes import *

if __name__ == "__main__":
    app.run(debug=True)

