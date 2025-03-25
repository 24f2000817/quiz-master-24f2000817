from app import app
from flask import render_template, request, redirect, url_for, flash, session
from controllers.database import *
from datetime import datetime

@app.route("/")
def home():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    return render_template("home.html", subjects = subjects, chapters = chapters, quizzes = quizzes, questions = questions)

@app.route("/add_subject" , methods = ["GET","POST"])
def add_subject():
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            return render_template("add_subject.html")
        
        if request.method == "POST":
            name = request.form.get("name",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("add_subject"))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("add_subject"))
            
            subject = Subject.query.filter_by(name = name).first()
            if subject:
                flash("Subject already exists")
                return redirect(url_for("add_subject"))
            
            new_subject = Subject(
                name = name,
                description = description
            )
            db.session.add(new_subject)
            db.session.commit()

            flash("Subject added successfully")

        return redirect(url_for("home"))

    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/add_chapter/<int:subject_id>" , methods = ["GET","POST"])
def add_chapter(subject_id):
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            # subjects = Subject.query.all()
            return render_template("add_chapter.html",subject_id = subject_id)
        
        if request.method == "POST":
            name = request.form.get("name",None)
            # subject_id = request.form.get("subject_id",None)
            description = request.form.get("description",None)

            if not name:
                flash("Name is required")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            # if not subject_id:
            #     flash("Subject is required")
            #     return redirect(url_for("add_chapter"))
            
            if not description:
                flash("Description is required")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            subject = Subject.query.filter_by(id = subject_id).first()
            if not subject:
                flash("Subject not found")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            chapter = Chapter.query.filter_by(name = name).first()
            if chapter:
                flash("Chapter already exists")
                return redirect(url_for("add_chapter",subject_id = subject_id))
            
            new_chapter = Chapter(
                name = name,
                subject_id = subject_id,
                description = description
            )

            db.session.add(new_chapter)
            db.session.commit()

            flash("Chapter added successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    

@app.route("/add_quiz" , methods = ["GET","POST"])
def add_quiz():
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            chapters = Chapter.query.all()
            return render_template("add_quiz.html",chapters = chapters)
        
        if request.method == "POST":
            chapters = Chapter.query.all()
            chapter_id = request.form.get("chapter_id",None)
            title = request.form.get("title",None)
            date_of_quiz = request.form.get("date",None)
            time_of_quiz = request.form.get("time",None)
            duration = request.form.get("duration",None)
            remarks = request.form.get("remarks",None)

            if not title:
                flash("Title is required")
                return redirect(url_for("add_quiz",chapters = chapters))

            if not chapter_id:
                flash("Chapter is required")
                return redirect(url_for("add_quiz",chapters = chapters))
            
            if not date_of_quiz:
                flash("Date is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            if not time_of_quiz:
                flash("Time is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            if not duration:
                flash("Duration is required")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            chapter = Chapter.query.filter_by(id = chapter_id).first()
            if not chapter:
                flash("Chapter not found")
                return redirect(url_for("add_quiz", chapters = chapters))
            
            date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()
            time_of_quiz = datetime.strptime(time_of_quiz, "%H:%M").time()
            duration = int(duration)

            new_quiz = Quiz(
                chapter_id = chapter_id,
                title = title,
                date_of_quiz = date_of_quiz,
                time_of_quiz = time_of_quiz,
                duration = duration,
                remarks = remarks
            )

            db.session.add(new_quiz)
            db.session.commit()

            flash("Quiz added successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/quiz_management")
def quiz_management():
    if session.get('user_role', None) == 'admin':
        quizzes = Quiz.query.all()
        questions = Question.query.all()
        return render_template("quiz_management.html", quizzes = quizzes, questions = questions)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))

@app.route("/add_question/<int:quiz_id>" , methods = ["GET","POST"])
def add_question(quiz_id):
    if session.get('user_role', None) == 'admin':
        if request.method == "GET":
            return render_template("add_question.html",quiz_id = quiz_id)
        
        if request.method == "POST":
            quiz = Quiz.query.filter_by(id = quiz_id).first()
            if not quiz:
                flash("Quiz not found")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            question_title = request.form.get("question_title",None)
            question_statement = request.form.get("question_statement",None)
            option1 = request.form.get("option1",None)
            option2 = request.form.get("option2",None)
            option3 = request.form.get("option3",None)
            option4 = request.form.get("option4",None)
            correct_option = request.form.get("correct_option",None)

            if not question_title:
                flash("Question title is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not question_statement:
                flash("Question statement is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option1:
                flash("Option1 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option2:
                flash("Option2 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not option3:
                flash("Option3 is required")
                return redirect(url_for("add_question", quiz_id = quiz_id))
            
            if not option4:
                flash("Option4 is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not correct_option:
                flash("Correct option is required")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if option1 == option2 or option1 == option3 or option1 == option4 or option2 == option3 or option2 == option4 or option3 == option4:
                flash("Options should be unique")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            if not (correct_option == option1 or correct_option == option2 or correct_option == option3 or correct_option == option4):
                flash("Invalid correct option")
                return redirect(url_for("add_question",quiz_id = quiz_id))
            
            new_question = Question(
                quiz_id = quiz_id,
                question_title = question_title,
                question_statement = question_statement,
                option1 = option1,
                option2 = option2,
                option3 = option3,
                option4 = option4,
                correct_option = correct_option
            )

            db.session.add(new_question)
            db.session.commit()

            flash("Question added successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_subject/<int:subject_id>")
def delete_subject(subject_id):
    if session.get('user_role', None) == 'admin':
        subject = Subject.query.filter_by(id = subject_id).first()
        if not subject:
            flash("Subject not found")
            return redirect(url_for("home"))
        
        db.session.delete(subject)
        db.session.commit()

        flash("Subject deleted successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    

@app.route("/delete_chapter/<int:chapter_id>")
def delete_chapter(chapter_id):
    if session.get('user_role', None) == 'admin':
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not chapter:
            flash("Chapter not found")
            return redirect(url_for("home"))
        
        db.session.delete(chapter)
        db.session.commit()

        flash("Chapter deleted successfully")

        return redirect(url_for("home"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    if session.get('user_role', None) == 'admin':
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash("Quiz not found")
            return redirect(url_for("quiz_management"))
        
        db.session.delete(quiz)
        db.session.commit()

        flash("Quiz deleted successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    if session.get('user_role', None) == 'admin':
        question = Question.query.filter_by(id = question_id).first()
        if not question:
            flash("Question not found")
            return redirect(url_for("quiz_management"))
        
        db.session.delete(question)
        db.session.commit()

        flash("Question deleted successfully")

        return redirect(url_for("quiz_management"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/users")
def users():
    if session.get('user_role', None) == 'admin':
        users = User.query.all()
        return render_template("users.html", users = users)
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if session.get('user_role', None) == 'admin':
        user = User.query.filter_by(id = user_id).first()
        if not user:
            flash("User not found")
            return redirect(url_for("home"))
        
        db.session.delete(user)
        db.session.commit()

        flash("User deleted successfully")

        return redirect(url_for("users"))
    
    else:
        flash("You are not authorized to access this page")
        return redirect(url_for("home"))
    
