from flask import Flask, render_template, request, redirect, url_for, flash
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import re
import os
import pdfplumber


import resume_parser
import resume_job_matcher


app = Flask(__name__)

# app.secret_key = "my_secret_key"

# Upload folder & allowed extensions
upload_folder = os.path.join(os.getcwd(), "uploads")
allowed_extensions = {'pdf'}
app.config['upload_folder'] = upload_folder


if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)


# Flask
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get resume text and job description text from form data
        resume_text = request.form.get("resume_text", "")
        job_description = request.form.get("job_description", "")

        # Error handling for not filled fields
        if not resume_text or not job_description:
            error = "Provide resume text AND job description!"
            return render_template("index.html", error=error)

        # Compute similarity score of resume text and job description
        score = resume_job_matcher.compute_similarity(resume_text, job_description)
        # For simplicity, show in percentage
        match_percentage = round(score * 100, 2)

        return render_template("index.html",
                               match_percentage=match_percentage,
                               resume_text=resume_text,
                               job_description=job_description)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
