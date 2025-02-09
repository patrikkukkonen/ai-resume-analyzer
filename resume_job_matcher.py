from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess_text import preprocess_text

# Matching function using TF-IDF and cosine similarity

def compute_similarity(resume_text, job_description):
    """
    Computes the cosine similarity between the resume text and the job description.

    Args:
        resume_text (str): The cleaned text extracted from the (pdf) resume.
        job_description (str): The job description text.

    Returns:
        float: Similarity score between 0 and 1.
    """

    # resume_text = preprocess_text(resume_text)
    # job_description = preprocess_text(resume_text)

    # Combine texts to build the TF-IDF vocabulary
    documents = [resume_text, job_description]

    # Initialize the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute cosine similarity between the two documents
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

    # The similarity score between resume and job description
    score = similarity_matrix[0][1]
    return score


if __name__ == "__main__":
    # Example texts (replace these with your actual cleaned texts)
    resume_text = """
    John Doe is an Software Engineer with expertise in Python, machine learning, 
    and web development. He has worked with frameworks like Django and Flask, and has a strong 
    background in data analysis.
    """

    job_description = """
    We are looking for a Software Engineer skilled in Python and web development. 
    Experience with Django or Flask and a strong understanding of machine learning techniques is required.
    """

    # Compute similarity
    similarity_score = compute_similarity(resume_text, job_description)
    print(f"Match Score: {similarity_score * 100:.2f}%")