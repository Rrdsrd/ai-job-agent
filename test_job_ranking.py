
from job_search import fetch_greenhouse_jobs, filter_jobs
from job_matcher import rank_jobs



COMPANIES = [
    "stripe",
    "figma",
    "airbnb",
    "opentable",
    "mariadbplc",
    "gatherai",
    "particle41llc",
    "precisionmedicinegroup",

    # New companies
    "yipitdata",
    "globalizationpartners"
]



all_jobs = []

print("\nFetching jobs from companies...\n")

for company in COMPANIES:

    try:
        jobs = fetch_greenhouse_jobs(company)
        all_jobs.extend(jobs)

        print(f"{company}: {len(jobs)} jobs found")

    except Exception as error:
        print(f"Error fetching {company}: {error}")


print(f"\nTotal jobs fetched: {len(all_jobs)}")


# Keep potential India/remote jobs matching your target titles
potential_jobs = filter_jobs(all_jobs)

print(f"\nPotential matching jobs: {len(potential_jobs)}")


# Rank jobs using candidate profile
print("\nRanking jobs using weighted matching...\n")

ranked_jobs = rank_jobs(potential_jobs)


# Display top 10 jobs
print("\n========== TOP 10 JOB MATCHES ==========\n")

for index, job in enumerate(ranked_jobs[:10], start=1):

    print(f"\nRANK: {index}")
    print(f"Title: {job.get('title')}")
    print(f"Company: {job.get('company')}")
    print(f"Location: {job.get('location')}")
    print(f"Match Score: {job.get('match_score')}/100")

    print(f"Scoring Method: {job.get('scoring_method')}")

    print(f"Matching Skills: {job.get('matching_skills')}")

    print(f"Mandatory Skills: {job.get('mandatory_skills')}")

    print(f"Preferred Skills: {job.get('preferred_skills')}")

    print(f"Not Confirmed: {job.get('not_confirmed')}")

    print(f"Apply Link: {job.get('url')}")

    print("-" * 60)
