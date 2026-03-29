# ResuMatch — AI-Powered Resume Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Upload your resume. Paste a job description. Know your fit score in seconds.**

[Features](#-features) · [How It Works](#-how-it-works) · [Evaluation](#-evaluation-results) · [Installation](#-installation) · [API](#-api-reference) · [Screenshots](#-screenshots)

</div>

---

## 🎯 What Is ResuMatch?

ResuMatch is a full-stack resume intelligence tool that analyzes how well your resume fits a given job description — without any neural network or paid API. It uses **TF-IDF semantic similarity**, **domain-aware skill extraction**, and **project relevance scoring** to produce a detailed compatibility report with actionable improvement suggestions.

Built entirely from scratch with a Django REST backend and a React frontend.

---

## ✨ Features

- 🔍 **Skill Gap Analysis** — Detects matched and missing skills across 24 industry domains
- 📊 **Multi-Dimensional Scoring** — Breaks down your score into Skill Match, Text Relevance, Experience Fit, and Project Score
- 📁 **PDF Resume Parsing** — Extracts clean text directly from uploaded PDF resumes using PyMuPDF
- 🧠 **Domain-Aware Skill Extraction** — Covers 200+ skills across IT, Legal, Aviation, Finance, Healthcare, Apparel, and more
- 💡 **Actionable Suggestions** — Tells you exactly which skills to add and what to improve
- ⚡ **Fast** — Full analysis in under 3 seconds
- 🎨 **Polished UI** — Animated score ring, confetti on high scores, live skill chips, and breakdown bars

---

## 🏗️ How It Works

```
User uploads PDF resume + pastes Job Description
                    │
                    ▼
        ┌───────────────────────┐
        │   PDF Text Extraction  │  ← PyMuPDF (fitz)
        └───────────┬───────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
   Skill Extraction      Experience Detection
   (200+ skills,         (regex year patterns)
    24 domains)
          │                    │
          └─────────┬──────────┘
                    ▼
        ┌───────────────────────┐
        │   Project Detection    │  ← action + object + metric patterns
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Scoring Engine       │
        │                       │
        │  35% Skill Match       │  ← set intersection over job skills
        │  25% Text Similarity   │  ← TF-IDF cosine similarity (1-2 ngrams)
        │  20% Experience Fit    │  ← years detected vs years required
        │  20% Project Score     │  ← per-project TF-IDF vs JD
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Final Report         │
        │  Score · Skills ·      │
        │  Gaps · Suggestions    │
        └───────────────────────┘
```

---

## 📈 Evaluation Results

Evaluated against **2,484 labeled resume-JD pairs** across **24 industry categories** using the [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset).

### Methodology

For each resume, the scorer was run against:
- Its **correct JD** (same category) → expected HIGH score
- A **randomly chosen wrong JD** (different category) → expected LOW score

**Accuracy = % of times the correct JD scored higher than the wrong JD**

### Overall Results

| Metric | Score |
|---|---|
| ✅ Overall Pairwise Accuracy | **84.8%** |
| 🏆 Best Category (Business Dev) | **98.3%** |
| 🏆 Best Category (HR) | **98.2%** |
| 📊 Total Resumes Tested | **2,484** |
| 🗂️ Industry Categories | **24** |

### Accuracy by Category

| Category | Accuracy |
|---|---|
| Business Development | 98.3% |
| HR | 98.2% |
| Finance | 96.6% |
| Accountant | 95.8% |
| Teacher | 95.1% |
| Construction | 94.6% |
| Healthcare | 92.2% |
| Chef | 89.8% |
| Consultant | 89.6% |
| Public Relations | 88.3% |
| Digital Media | 87.5% |
| BPO | 86.4% |
| Sales | 86.2% |
| Designer | 86.0% |
| Banking | 84.3% |
| Fitness | 82.1% |
| Information Technology | 80.8% |
| Engineering | 80.5% |
| Aviation | 79.5% |
| Automobile | 77.8% |
| Arts | 73.8% |
| Apparel | 65.0% |
| Agriculture | 60.3% |
| Advocate | 48.3% |

### Key Insight

> Pure TF-IDF + keyword matching achieves **84.8% pairwise ranking accuracy** across 24 domains **without any neural network or pretrained embeddings**. Categories with overlapping vocabulary (legal/banking, arts/media) represent the natural ceiling of keyword-based approaches — a known limitation documented in IR literature.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, CSS3 animations |
| Backend | Django 4, Django REST Framework |
| PDF Parsing | PyMuPDF (fitz) |
| NLP / Scoring | scikit-learn TF-IDF, cosine similarity |
| Skill Extraction | Custom regex over 200+ domain skills |
| Dataset (eval) | Kaggle Resume Dataset — 2,484 resumes, 24 categories |

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/resumatch.git
cd resumatch

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### Requirements

```
django
djangorestframework
django-cors-headers
pymupdf
scikit-learn
numpy
pandas
fpdf2
```

---

## 📡 API Reference

### `POST /api/match/`

Analyzes a resume against a job description.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `resume` | File (PDF) | The resume to analyze |
| `job_description` | String | Full job description text |

**Response** — `application/json`

```json
{
  "score": 78.4,
  "skill_score": 83.2,
  "text_score": 71.5,
  "experience_score": 100.0,
  "projects_score": 62.1,
  "experience_years": 4.0,
  "projects_count": 3,
  "resume_skills": ["python", "django", "postgresql", "docker"],
  "matched_skills": ["python", "django"],
  "missing_skills": ["kubernetes", "aws", "react"],
  "suggestions": [
    "Your resume matches the job well.",
    "Consider adding skills: kubernetes, aws, react",
    "Include more real-world or domain-specific projects."
  ]
}
```

---

## 📁 Project Structure

```
resumatch/
│
├── backend/
│   ├── matcher/
│   │   ├── utils/
│   │   │   ├── parser.py          # PDF extraction, experience & project detection
│   │   │   ├── matcher.py         # TF-IDF scoring, cosine similarity
│   │   │   ├── skills.py          # 200+ domain skill definitions
│   │   │   └── suggestions.py     # Suggestion generator
│   │   ├── match_service.py       # Main orchestration layer
│   │   └── views.py               # REST API endpoint
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx           # Main app component
│   │   │   └── Home.css           # All styles
│   └── package.json
│
└── evaluation/
    ├── evaluate.py                # Dataset exploration
    ├── score_resumes.py           # Full evaluation pipeline
    ├── job_descriptions.py        # 24 category JDs
    └── evaluation_results.csv     # Full results (2484 rows)
```

---

## 🧪 Running the Evaluation

```bash
cd evaluation

# Install eval dependencies
pip install pandas fpdf2 requests

# Make sure Django is running, then:
python score_resumes.py
```

This runs all 2,484 resumes through your live API and outputs accuracy per category.

---

## ⚠️ Limitations

- **PDF only** — Does not support `.docx` or `.txt` resumes
- **English only** — Skill extraction is English-language based
- **Keyword ceiling** — TF-IDF approaches a natural ~85% accuracy ceiling on cross-domain tasks; semantic embeddings (e.g. sentence-transformers) would push this higher
- **Score is relative** — The score reflects fit vs the provided JD, not an absolute employability score

---

## 🔮 Future Improvements

- [ ] Upgrade skill matching to sentence-transformers for semantic understanding
- [ ] Add support for `.docx` resume format
- [ ] Browser extension to analyze job postings directly on LinkedIn / Naukri
- [ ] ATS simulation mode — score resume as an Applicant Tracking System would
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Resume rewrite suggestions powered by LLM

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Made with ☕ and Python

⭐ Star this repo if you found it useful!

</div>
