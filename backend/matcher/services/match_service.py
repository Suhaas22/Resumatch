from matcher.utils.parser import (
    extract_resume_text,
    extract_experience,
    extract_projects,
    extract_required_experience
)
from matcher.utils.matcher import get_match_score, get_project_similarity_score
from matcher.utils.skills import extract_skills


def process_match(resume_file, job_description):

    # text extraction
    resume_text = extract_resume_text(resume_file)
    print("resume extracted")

    # skills extraction
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    required_experience = extract_required_experience(job_description)

    print("skills extracted")

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))
    print("list of skills extracted")

    # experience and project extractions
    experience_years = extract_experience(resume_text)
    projects = extract_projects(resume_text)
    projects_count = min(len(projects), 6)
    projects_score = get_project_similarity_score(projects, job_description)

    projects_score = (0.8 * projects_score) + (0.2 * min(projects_count * 30, 100))
    print("exp years and projects count done")

    # scores
    scores = get_match_score(resume_text, job_description, resume_skills, job_skills, 
                            experience_years, projects_score, required_experience)

    score = scores["final_score"]

    print("score calculation done")

    print("Required Experience:", required_experience)

    # suggestions
    suggestions = []

    if score > 80:
        suggestions.append("Your resume matches the job well.")
    else:
        suggestions.append("Improve your resume for better match.")

    if missing_skills:
        suggestions.append(
            "Consider adding skills: " + ", ".join(missing_skills)
        )

    if scores["experience_score"] < 60:
        suggestions.append("Add more relevant work experience or internships.")

    if scores["projects_score"] < 60:
        suggestions.append("Include more real-world or domain-specific projects.")

    print("suggestions done")
    print(score)

    print(scores)

    print("Detected Projects:")
    for p in projects:
        print("-", p)

    return {
        "score": float(score),

        "skill_score": float(scores["skill_score"]),
        "text_score": float(scores["text_score"]),
        "experience_score": float(scores["experience_score"]),
        "projects_score": float(scores["projects_score"]),  

        "experience_years": float(experience_years),
        "projects_count": int(projects_count),

        "resume_skills": list(resume_skills),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),

        "suggestions": list(suggestions),
    }