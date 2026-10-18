# Resume Screening Automation (NLP & ATS)

A turnkey Natural Language Processing (NLP) web application for automated resume screening and candidate-job matching.

## Features
- **TF-IDF & Cosine Similarity**: Measures contextual overlap between candidate resume and target Job Description.
- **Skill Extraction**: Matches against 150+ industry technical competencies across Python, ML, Cloud, and Web Development.
- **ATS Gap Analysis**: Identifies matched and missing skills with actionable resume optimization recommendations.
- **Turnkey Setup**: Zero external model downloads required.

## Installation & Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the web application
python app.py
```
Open your browser at `http://127.0.0.1:5000`.
