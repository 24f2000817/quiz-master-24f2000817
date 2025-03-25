
from flask import Flask, render_template
from controllers.database import db, User
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

from controllers.authentication import *
from controllers.routes import *
from controllers.edit_routes import *

def no_of_questions(chapter_id):
    chapter = Chapter.query.filter_by(id = chapter_id).first()

    no_of_questions = sum([len(quiz.questions) for quiz in chapter.quizzes])
    return no_of_questions

app.jinja_env.globals.update(no_of_questions = no_of_questions)

if __name__ == "__main__":
    app.run(debug=True)

