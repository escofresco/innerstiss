import os

from flask import flash, redirect, render_template, request, url_for
from werkzeug import secure_filename
from app import app

def file_is_valid(filename):
    return True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def upload():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file and file_is_valid(file.filename):
                filename = secure_filename(file.filename)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save("tmp/"+filename)
                flash("Upload successful")
                return redirect(url_for("home"))
        flash("Oh no...a file wasn't uploaded.")
        return redirect(request.url)os.path.
