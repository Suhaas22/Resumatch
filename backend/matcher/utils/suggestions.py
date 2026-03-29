def generate_suggestions(projects_count, missing_skills):

    suggestions = []

    if projects_count < 3:
        suggestions.append(f"Consider adding more projects using required skills for this job.")


    if not missing_skills:
        return [
            "Your resume matches the job well.",
            "Add real-world experience or internships to strengthen your profile."
        ]


    for skill in missing_skills:
        suggestions.append(f"Consider learning {skill} to improve your profile.")

    return suggestions