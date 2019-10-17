import os

from flask import flash, redirect, render_template, request, url_for
from werkzeug import secure_filename

from app import app
import helper


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
                file.save("tmp/" + filename)
                flash("Upload successful")
                #return redirect(url_for("home"))
                return redirect(
                    url_for("view_transcription", transcription_id="someid"))
        flash("Oh no...a file wasn't uploaded.")
        return redirect(request.url)


@app.route("/<transcription_id>")
def view_transcription(transcription_id):
    try:
        transcription = helper.transcription_by_id(transcription_id)
        return render_template("transcription_view.html",
                               title=transcription["title"],
                               transcription_name=sample_title,
                               transcription_content=sample_content)
    except:
        return render_template("error_view.html")
