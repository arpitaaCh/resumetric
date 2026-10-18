
import re

SKILLS = {
    "Languages": [
        "Python", "Java", "JavaScript", "TypeScript",
        "C++", "C#", "SQL", "Go", "Rust"
    ],
    "Frameworks": [
        "Django", "Flask", "FastAPI", "React",
        "Angular", "Spring Boot", "Streamlit"
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB",
        "Redis", "SQLite"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker",
        "Kubernetes", "Git", "GitHub", "CI/CD"
    ],
    "Data & AI": [
        "Machine Learning", "Deep Learning",
        "NLP", "Pandas", "NumPy",
        "TensorFlow", "PyTorch"
    ],
    "Engineering": [
        "REST API", "Unit Testing",
        "Software Testing", "Debugging",
        "Data Structures", "Algorithms"
    ]
}


def normalize(text):
    return re.sub(r"\s+", " ", text.lower())


def extract_skills(text):
    text = normalize(text)
    detected = []

    aliases = {
        "REST API": ["rest api", "restful api", "rest apis"],
        "CI/CD": ["ci/cd", "continuous integration"],
    }

    for category, skills in SKILLS.items():
        for skill in skills:
            terms = aliases.get(skill, [skill.lower()])

            for term in terms:
                pattern = (
                    r"(?<!\w)"
                    + re.escape(term)
                    + r"(?!\w)"
                )

                if re.search(pattern, text):
                    detected.append({
                        "skill": skill,
                        "category": category
                    })
                    break

    return detected


def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    resume_set = {
        item["skill"] for item in resume_skills
    }

    job_set = {
        item["skill"] for item in job_skills
    }

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    coverage = (
        round(len(matched) / len(job_set) * 100)
        if job_set else None
    )

    return {
        "coverage": coverage,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_set),
        "job_skills": sorted(job_set)
    }
