from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_text_similarity(resume_text, job_desc):

    tfidf = TfidfVectorizer(stop_words="english", ngram_range = (1, 2), max_features = 5000)
    vectors = tfidf.fit_transform([resume_text, job_desc])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    print("get_text_similarity done")

    return similarity[0][0] * 100

def get_match_score(resume_text, job_desc, resume_skills, job_skills,
                     experience_years, projects_score, required_exp):

    text_score = get_text_similarity(resume_text, job_desc)

    if len(job_skills) == 0:
        skill_score = 0
    else:
        matched = set(resume_skills) & set(job_skills)
        skill_score = (len(matched) / len(job_skills)) * 100

    if required_exp == 0:
        experience_score = 50  
    elif experience_years >= required_exp:
        experience_score = 100
    else:
        experience_score = (experience_years / required_exp) * 100

    final_score = (0.35 * skill_score + 0.25 * text_score + 
                    0.20 * experience_score + 0.20 * projects_score)

    print("return final score done")

    return {
        "final_score": float(round(final_score, 2)),
        "skill_score": float(round(skill_score, 2)),
        "text_score": float(round(text_score, 2)),
        "experience_score": float(round(experience_score, 2)),
        "projects_score": float(round(projects_score, 2)), 
    }

def get_project_similarity_score(projects, job_desc):
    if not projects:
        return 0.0

    scores = []

    for project in projects:
        try:
            tfidf = TfidfVectorizer(stop_words = 'english')
            vecs = tfidf.fit_transform([project, job_desc])

            sim = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
            scores.append(sim)

        except Exception as e:
            print("Project similarity error:", e)
            continue

    if not scores:
        return 0.0            

    avg_score = sum(scores)/len(scores)
    return round(avg_score * 100, 2)

