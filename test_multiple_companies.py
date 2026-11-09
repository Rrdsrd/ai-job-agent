from job_search import fetch_greenhouse_jobs, filter_jobs

COMPANIES = [
    "stripe",
    "figma",
    "airbnb",
    "opentable",
    "mariadbplc",
    "gatherai"
]

all_jobs = []

for company in COMPANIES:
    print(f"\nSearching jobs at {company}...")

    try:
        jobs = fetch_greenhouse_jobs(company)

        print("Jobs retrieved:", len(jobs))

        for job in jobs:
            job["company"] = company

        all_jobs.extend(jobs)

    except Exception as error:
        print(f"Could not retrieve jobs from {company}: {error}")

matching_jobs = filter_jobs(all_jobs)

print("\n================================")
print("TOTAL JOBS:", len(all_jobs))
print("MATCHING JOBS:", len(matching_jobs))
print("================================")

for job in matching_jobs:
    print("\n-----------------------------")
    print("Title:", job["title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Eligibility:", job["eligibility_status"])
    print("Apply here:", job["url"])