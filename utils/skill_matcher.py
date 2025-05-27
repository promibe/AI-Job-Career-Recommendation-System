import json
from fuzzywuzzy import fuzz

def load_skill_gap_data():
    with open("data/skill_gap.json", 'r') as f:
        return json.load(f)

def extract_skills(resume_text, skill_set, fuzzy_threshold=90):
    resume_text = resume_text.lower()
    matched_skills = set()

    for skill in skill_set:
        if skill.lower() in resume_text:
            matched_skills.add(skill)
        else:
            ratio = fuzz.partial_ratio(skill.lower(), resume_text)
            if ratio >= fuzzy_threshold:
                matched_skills.add(skill)

    remaining_skills = [skill for skill in skill_set if skill not in matched_skills]
    percentage_gap = (len(matched_skills) / len(skill_set)) * 100 if skill_set else 0
    return sorted(list(matched_skills)), remaining_skills, percentage_gap
