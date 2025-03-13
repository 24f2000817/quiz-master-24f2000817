
from flask import Flask, render_template
from database import (
    db
)

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

