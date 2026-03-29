import fitz
import re


def extract_resume_text(file):
    text = ""

    try:
        file_bytes = file.read()
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text

    except Exception as e:
        raise Exception(f"PDF parsing error: {str(e)}")


def extract_experience(text):
    matches = re.findall(r'(\d+\.?\d*)\+?\s*(years|yrs)', text.lower())

    if matches:
        return max([float(m[0]) for m in matches])

    return 0
def extract_projects(resume_text):
    text = resume_text.lower()
    sentences = re.split(r'[.\n]', text)

    projects = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 40:
            continue

        has_action = any(word in sentence for word in [
            "developed", "created", "built", "implemented", "designed"
        ])

        has_object = any(word in sentence for word in [
            "system", "application", "platform", "tool", "website"
        ])

        has_metrics = bool(re.search(r'\d+%', sentence))

        is_process = any(word in sentence for word in [
            "process", "workflow", "meeting"
        ])

        if has_action and has_object and not is_process:
            
            if has_metrics:
                projects.append(sentence)

            elif len(sentence.split()) > 8:
                projects.append(sentence)

    return projects


def extract_required_experience(text):
    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*(?:years|yrs)',                     # direct case
        r'(\d+)\s*-\s*(\d+)\s*(?:years|yrs)',            # range case
        r'at least\s*(\d+)\s*(?:years|yrs)',             # at least case
        r'minimum\s*(\d+)\s*(?:years|yrs)',              # minimum case
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            if isinstance(match, tuple):
                values.append(int(match[-1]))
            else:
                values.append(int(match))

    if values:
        return max(values)

    return 0
