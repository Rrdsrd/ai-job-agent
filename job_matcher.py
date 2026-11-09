
import re
import html


SKILL_KEYWORDS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "AWS": ["aws", "amazon web services"],
    "Snowflake": ["snowflake"],
    "ETL": ["etl", "extract transform load"],
    "Data Pipelines": ["data pipelines", "data pipeline"],
    "Apache Airflow": ["airflow", "apache airflow"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "React.js": ["react.js", "reactjs"],
    "LangGraph": ["langgraph"],
    "Kafka": ["kafka", "apache kafka"],
    "Databricks": ["databricks"],
    "Apache Spark": ["apache spark", "pyspark"],
    "Delta Lake": ["delta lake"],
    "RAG": ["rag", "retrieval augmented generation"],
    "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex"],
    "Vector Databases": ["vector database", "vector databases"],
    "MLflow": ["mlflow"],
    "Unity Catalog": ["unity catalog"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"]
}

PREFERRED_WORDS = [
    "preferred",
    "preferably",
    "nice to have",
    "nice-to-have",
    "bonus",
    "a plus",
    "desirable",
    "would be beneficial",
    "ideally"
]

REQUIRED_WORDS = [
    "required",
    "must have",
    "must-have",
    "minimum qualifications",
    "basic qualifications",
    "you have",
    "you should have",
    "strong experience",
    "proficiency in",
    "proficient in"
]


def clean_text(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def find_skills(text):
    found = []

    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

            if re.search(pattern, text):
                found.append(skill)
                break

    return found


def classify_skill(skill, description):
    """
    Classify a skill using nearby job-description wording.
    This is a heuristic, not a perfect understanding of the JD.
    """

    keywords = SKILL_KEYWORDS[skill]
    sentences = re.split(r"[.!?\n;]", description)

    evidence = []

    for sentence in sentences:
        for keyword in keywords:
            pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

            if re.search(pattern, sentence):
                evidence.append(sentence)
                break

    if any(
        any(word in sentence for word in PREFERRED_WORDS)
        for sentence in evidence
    ):
        return "preferred"

    if any(
        any(word in sentence for word in REQUIRED_WORDS)
        for sentence in evidence
    ):
        return "mandatory"

    return "unclassified"


def evaluate_job(job, profile_text):

    description = clean_text(job.get("description", ""))
    profile = clean_text(profile_text)

    candidate_skills = find_skills(profile)
    job_skills = find_skills(description)

    matching = []
    mandatory = []
    preferred = []
    unclassified = []

    for skill in job_skills:

        category = classify_skill(skill, description)

        if skill in candidate_skills:
            matching.append(skill)

        if category == "mandatory":
            mandatory.append(skill)

        elif category == "preferred":
            preferred.append(skill)

        else:
            unclassified.append(skill)

    mandatory_matches = [
        skill for skill in mandatory
        if skill in candidate_skills
    ]

    preferred_matches = [
        skill for skill in preferred
        if skill in candidate_skills
    ]

    # Weighted score: mandatory = 70%, preferred = 30%.
    # If only one category is identified, normalize its score
    # to 100% rather than penalizing the missing category.

    available_weight = 0
    weighted_points = 0

    if mandatory:
        available_weight += 70
        weighted_points += (
            len(mandatory_matches) / len(mandatory)
        ) * 70

    if preferred:
        available_weight += 30
        weighted_points += (
            len(preferred_matches) / len(preferred)
        ) * 30

    if available_weight:
        score = round(weighted_points / available_weight * 100)
        scoring_method = "Weighted mandatory/preferred skills"
    elif job_skills:
        score = round(len(matching) / len(job_skills) * 100)
        scoring_method = "Equal-weight keyword fallback"
    else:
        score = 0
        scoring_method = "No detectable skills in job description"

    return {
        **job,
        "match_score": score,
        "scoring_method": scoring_method,
        "matching_skills": matching,
        "mandatory_skills": mandatory,
        "mandatory_matches": mandatory_matches,
        "preferred_skills": preferred,
        "preferred_matches": preferred_matches,
        "unclassified_skills": unclassified,
        "not_confirmed": [
            skill for skill in job_skills
            if skill not in candidate_skills
        ]
    }


def rank_jobs(jobs, profile_file="candidate_profile.txt"):

    with open(profile_file, "r", encoding="utf-8") as file:
        profile_text = file.read()

    ranked_jobs = [
        evaluate_job(job, profile_text)
        for job in jobs
    ]

    # Highest match score first
    ranked_jobs.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return ranked_jobs


def analyze_job_match(job, profile_file="candidate_profile.txt"):

    ranked = rank_jobs([job], profile_file)
    result = ranked[0]

    return f"""
========== JOB MATCH REPORT ==========

Job: {result.get('title', 'Unknown')}
Company: {result.get('company', 'Unknown')}
Location: {result.get('location', 'Unknown')}

MATCH SCORE: {result['match_score']}/100
Scoring method: {result['scoring_method']}

MANDATORY SKILLS:
{result['mandatory_skills']}

CONFIRMED MANDATORY MATCHES:
{result['mandatory_matches']}

PREFERRED SKILLS:
{result['preferred_skills']}

CONFIRMED PREFERRED MATCHES:
{result['preferred_matches']}

OTHER SKILLS MENTIONED:
{result['unclassified_skills']}

NOT CONFIRMED:
{result['not_confirmed']}

Note: Not confirmed means absent from the candidate profile,
not necessarily that the candidate lacks the skill.

======================================
"""
