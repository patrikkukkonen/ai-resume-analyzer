import re


def clean_text(text):
    """Normalize whitespace. Remove unnecessary spaces, tabs and newlines"""
    cleaned = " ".join(text.split())
    return cleaned


def merge_line_breaks(text):
    """
    Replace line breaks that are in the middle of a sentence.
    This function looks for line breaks that are not preceded by punctuation.
    """
    # Replace line breaks not preceded by punctuation with a space.
    # Look for a newline that is not immediately after . ! or ?.
    merged = re.sub(r'(?<![.!?])\n', ' ', text)
    # Also remove any extra spaces created after merging
    merged = " ".join(merged.split())
    return merged


def preprocess_text(text):
    # Step 1: Merge line breaks that are not real sentence endings.
    text = merge_line_breaks(text)
    # Step 2: Clean the text by removing extra whitespace.
    text = clean_text(text)
    return text
