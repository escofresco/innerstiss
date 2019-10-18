import os

from botocore.exceptions import ClientError
from flask import flash, redirect, render_template, request, session, url_for
from werkzeug import secure_filename

from app import app
import helpers


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def upload():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file and helpers.file_is_valid(file.filename):
                filename = secure_filename(file.filename)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filepath = "tmp/" + filename
                file.save(filepath)
                flash("Upload successful")
                try:
                    upload_res = helpers.upload_to_s3(filepath, filename)
                except ClientError as e:
                    return render_template("error_view.html",
                                           error_message=str(e))
                try:
                    transcribe_res = helpers.transcribe(filename)
                except ClientError as e:
                    return render_template("error_view.html",
                                           error_message=str(e))
                transcript_uri = transcribe_res["TranscriptionJob"][
                    "Transcript"]["TranscriptFileUri"]
                session[filename] = helpers.load_json_from_uri(transcript_uri)
                #helpers.remove_from_s3(filename)
                return redirect(
                    url_for("view_transcript", transcript_id=filename))
        flash("Oh no...a file wasn't uploaded.")
        return redirect(request.url)


@app.route("/<transcript_id>")
def view_transcript(transcript_id):
    try:
        transcript = helpers.transcript_by_id(transcript_id)
        return render_template(
            "transcript_view.html",
            transcript_title=transcript["transcript_title"],
            transcript_content=transcript["transcript_content"])
    except FileNotFoundError as e:
        return render_template("error_view.html", error_message=str(e))
