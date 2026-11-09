
from job_search import fetch_greenhouse_jobs
from job_matcher import analyze_job_match

# Retrieve OpenTable vacancies
jobs = fetch_greenhouse_jobs("opentable")

# Find our India-remote Data Engineer vacancy
target_job = next(
    (
        job for job in jobs
        if "Senior Data Engineer (AI/ML)" in job["title"]
        and "india" in job["location"].lower()
    ),
    None
)

if target_job:
    print("Job found!")
    print("Title:", target_job["title"])
    print("Location:", target_job["location"])

    print("\nAnalyzing job using AI...")

    result = analyze_job_match(target_job)

    print("\n========== AI MATCH REPORT ==========")
    print(result)

else:
    print("Target job not found. It may have expired.")
