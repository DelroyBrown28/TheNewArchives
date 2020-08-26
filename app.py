import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main_blog_page")
def main_blog_page():
    return render_template("main_blog_page.html")


@app.route("/send_blog_post", methods=["POST", "GET"])
def send_blog_post():
    if request.method == "POST":
        blog_post = {
            "blog_title": request.form.get("blog_title"),
            "blog_body": request.form.get("blog_body"),
        }
        mongo.db.to_blog_posts.insert_one(blog_post)
        return redirect(url_for("send_blog_post"))
    details = mongo.db.to_blog_posts.find().sort("to_blog_posts", 1)
    return render_template("main_blog_page.html", blog_post=details)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
