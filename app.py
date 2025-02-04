from flask import Flask, render_template, request, redirect, url_for, flash
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import re
import os
import pdfplumber

from extract_pdf import extract_text_from_pdf
import resume_parser
from resume_job_matcher import compute_similarity


app = Flask(__name__)

# app.secret_key = "my_secret_key"

# Upload folder & allowed extensions
upload_folder = os.path.join(os.getcwd(), "uploads")
allowed_extensions = {'pdf'}  # allow only pdf (for now)
app.config['upload_folder'] = upload_folder


if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


# Flask
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get resume text and job description text from form data
        resume_text = request.form.get("resume_text", "")
        job_description = request.form.get("job_description", "")
        pdf_file = request.files.get("pdf_file")

        # Error handling for not filled fields
        if not job_description:  # not resume_text or
            error = "Provide job description!"
            return render_template("index.html", error=error)

        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['upload_folder'], filename)
            pdf_file.save(pdf_path)
            extracted_text = extract_text_from_pdf(pdf_path)
            # Delete file after extraction (optional)
            # os.remove(pdf_path)
            resume_text = extracted_text
        elif not resume_text:
            # If no PDF nor text provided, return error
            error = "Upload a PDF or paste a resume text"
            return render_template("index.html", error=error)

        # Compute similarity score of resume text and job description
        score = compute_similarity(resume_text, job_description)
        # For simplicity, show in percentage
        match_percentage = round(score * 100, 2)

        return render_template("index.html",
                               match_percentage=match_percentage,
                               resume_text=resume_text,
                               job_description=job_description)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
