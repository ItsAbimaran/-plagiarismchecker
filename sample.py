import re
import math
import streamlit as st
from collections import Counter

st.markdown(f'<h1 style="color:#40B5AD;">plagiarism checker</h1>', unsafe_allow_html=True)
def preprocess_text(text):
    # Tokenize and preprocess the text
    text = text.lower()
    text = re.sub(r'[^a-z ]', '', text)
    words = text.split()
    return Counter(words)

import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def cosine_similarity(vec1, vec2):
    # Calculate the cosine similarity between two text vectors
    intersection = set(vec1) & set(vec2)
    numerator = sum(vec1[word] * vec2[word] for word in intersection)
    sum1 = sum(vec1[word] ** 2 for word in vec1)
    sum2 = sum(vec2[word] ** 2 for word in vec2)
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def check_plagiarism(input_text, known_sources):
    input_vector = preprocess_text(input_text)
    plagiarism_matches = []

    for source_name, source_text in known_sources.items():
        source_vector = preprocess_text(source_text)
        similarity = cosine_similarity(input_vector, source_vector)
        
        if similarity > 0.7:  # You can adjust the threshold
            plagiarism_matches.append((source_name, similarity))

    return plagiarism_matches

if __name__ == "__main__":
    # Sample known sources (you should have a database)
    known_sources = {
        "Source1": "The cat chased the mouse around the house.",
        "Source2": "The universe is a vast, intricate tapestry of matter, energy, and phenomena awaiting exploration",
    }

    # Input text to check for plagiarism
    title=st.text_input("**enter the text**")

    plagiarism_matches = check_plagiarism(title, known_sources)
    if st.button("click"):
        if plagiarism_matches:
           print("Plagiarism Detected:")
           for source_name, similarity in plagiarism_matches:
               st.write(f"Source: {source_name}, Similarity: {similarity}")
        else:
            st.write("No plagiarism detected.")