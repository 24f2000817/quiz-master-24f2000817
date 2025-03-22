
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

@app.route("/")
def home():
    return render_template("home.html")

from controllers.authentication import *

if __name__ == "__main__":
    app.run(debug=True)

