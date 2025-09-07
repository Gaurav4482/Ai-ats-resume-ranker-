import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import fitz

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    elif ext == ".docx":
        text = docx2txt.process(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text

def rank_resumes(job_desc, resume_paths):
    documents = [job_desc]
    resume_texts = []
    for path in resume_paths:
        resume_texts.append(extract_text(path))
    documents.extend(resume_texts)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    results = []
    for idx, score in enumerate(similarity):
        results.append((os.path.basename(resume_paths[idx]), round(score*100, 2)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results
