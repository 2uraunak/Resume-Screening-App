import os
import re
import json
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

with open('skills.json', 'r', encoding='utf-8') as f:
    SKILLS_DATA = json.load(f)
ALL_SKILLS = set([s.lower() for s in SKILLS_DATA['technical_skills']])

def clean_text(text):
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def extract_skills(text):
    clean = clean_text(text)
    words = set(clean.split())
    found = []
    for s in SKILLS_DATA['technical_skills']:
        s_lower = s.lower()
        if ' ' in s_lower:
            if s_lower in clean:
                found.append(s)
        else:
            if s_lower in words:
                found.append(s)
    return sorted(list(set(found)))

@app.route('/')
def index():
    return render_template('index.html', roles=list(SKILLS_DATA['roles'].keys()))

@app.route('/screen', methods=['POST'])
def screen():
    data = request.get_json() if request.is_json else request.form
    resume_text = data.get('resume', '').strip()
    job_desc = data.get('job_desc', '').strip()
    target_role = data.get('role', '')

    if not resume_text or not job_desc:
        return jsonify({'error': 'Please provide both resume text and job description.'}), 400

    # TF-IDF Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_pct = round(float(sim) * 100, 1)

    # Skill matching
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    matched_skills = [s for s in jd_skills if s in resume_skills]
    missing_skills = [s for s in jd_skills if s not in resume_skills]

    # Role specific skills if selected
    role_coverage = None
    if target_role and target_role in SKILLS_DATA['roles']:
        req_skills = SKILLS_DATA['roles'][target_role]
        role_matched = [s for s in req_skills if s in resume_skills]
        role_coverage = {
            'role': target_role,
            'coverage_pct': round((len(role_matched) / len(req_skills)) * 100, 1),
            'matched': role_matched,
            'missing': [s for s in req_skills if s not in resume_skills]
        }

    # Actionable suggestions
    suggestions = []
    if match_pct < 50:
        suggestions.append("Low keyword alignment: Incorporate domain terminology directly from the job description.")
    if missing_skills:
        suggestions.append(f"Missing core competencies: Add project or practical experience mentioning {', '.join(missing_skills[:4])}.")
    if len(resume_skills) < 5:
        suggestions.append("Sparse technical vocabulary: Explicitly list your programming languages, libraries, and frameworks.")
    if not suggestions:
        suggestions.append("Outstanding match! Your resume closely reflects the technical requirements of this position.")

    return jsonify({
        'match_percentage': match_pct,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'resume_skills': resume_skills,
        'jd_skills': jd_skills,
        'role_coverage': role_coverage,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
