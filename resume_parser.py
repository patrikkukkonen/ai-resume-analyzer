import spacy
import re

# Load spaCy model
# English fast model: python -m spacy download en_core_web_sm / larger model en_core_web_trf
# Finnish fast model: python -m spacy download fi_core_news_sm
nlp = spacy.load("en_core_web_sm")  # use: en_core_web_sm or en_core_web_trf
nlp_fi = spacy.load("fi_core_news_sm")


def remove_non_ascii(text):
    return text.encode("ascii", errors="ignore").decode()


def extract_email(text):
    """Extract email addresses using regex."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails


def extract_phone(text):
    """Extract phone number using regex."""
    phone_pattern = r'\b[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}\b'
    phones = re.findall(phone_pattern, text)
    return phones


def extract_entities(text):
    """Extract entities from text using spaCy."""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# Process sample resume text
def parse_resume(text):
    """Extract useful resume information from the text."""
    emails = extract_email(text)
    phones = extract_phone(text)
    entities = extract_entities(text)

    # Filter entities by type (if needed)
    names = [ent[0] for ent in entities if ent[1] == "PERSON"]
    dates = [ent[0] for ent in entities if ent[1] == "DATE"]
    organizations = [ent[0] for ent in entities if ent[1] == "ORG"]
    languages = [ent[0] for ent in entities if ent[1] == "LANGUAGE"]
    locations = [ent[0] for ent in entities if ent[1] == "GPE"]

    # Extract entities (names, email, details etc.
    resume_info = {
        "emails": emails,
        "phones": phones,
        "names": names,
        "dates": dates,
        "languages": languages,
        "locations": locations,
        "organizations": organizations,
        "all_entities": entities
    }

    return resume_info


if __name__ == "__main__":
    # Example resume text (you can replace this with actual file input later)
    sample_text = """
    John Doe
    Email: john.doe@example.com
    Experience: Worked at OpenAI from January 2020 to March 2023.
    Education: B.Sc. in Computer Science from MIT.
    """

    # info = parse_resume(sample_text)
    print("Extracted Resume Information:")
    # for key, value in info.items():
    #    print(f"{key.capitalize()}: {value}")

    # info = parse_resume(extract_pdf("resume.pdf"))
    # for key, value in info.items():
    #    print(f"{key.capitalize()}: {value}")

    # print("Cleaned: ", clean_text(extract_pdf("resume.pdf")))
