from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/home")
def home():
    return render_template("home.html")

@main.route("/about")
def about():
    return render_template("about.html")
