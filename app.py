from flask import Flask, render_template, request, make_response, redirect, url_for, flash
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

app.secret_key = "my_secret_key"

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

@app.route('/set_theme/<theme>')
def set_theme(theme):
    response = make_response(redirect(url_for('index')))
    response.set_cookie('theme', theme, max_age=60*60*24*30)  # Store cookie for 30 days
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    theme = request.cookies.get('theme', 'dark')  # Default to 'dark' if no cookie is found

    # Toggle dark/light mode (for future)
    #if request.method == 'POST':
    #    theme = 'dark' if request.form.get('theme') == 'on' else 'light'
    #    response = make_response(render_template('index.html', theme=theme))
    #    response.set_cookie('theme', theme, max_age=60*60*24*30)  # Store cookie for 30 days
    #    return response



    # if 'theme' not in session:
    #    session['theme'] = 'dark'  # Default theme

    # if request.method == 'POST':
    #    session['theme'] = 'dark' if request.form.get('theme') == 'on' else 'light'

    if request.method == "POST":
        # Get resume text and job description text from form data
        resume_text = request.form.get("resume_text", "")
        job_description = request.form.get("job_description", "")
        print(f"job_desc: {job_description}")
        pdf_file = request.files.get('pdf_file')
        print(f'pdf_file: {pdf_file}')

        # Error handling for not filled fields
        if not job_description:  # not resume_text or
            error = "Provide job description!"
            print("Error happened!")
            return render_template("index.html", error=error)

        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['upload_folder'], filename)
            pdf_file.save(pdf_path)
            extracted_text = extract_text_from_pdf(pdf_path)
            # Delete file after extraction (optional)
            os.remove(pdf_path)
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

    return render_template("index.html", theme=theme)


if __name__ == "__main__":
    app.run(debug=True)
