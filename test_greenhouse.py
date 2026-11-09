from job_search import fetch_greenhouse_jobs, filter_jobs
import requests

# Enter a real Greenhouse board token
company_token = input("Enter company board token: ").strip()

try:
    # Step 1: Fetch real jobs
    jobs = fetch_greenhouse_jobs(company_token)

    print("\nTotal jobs retrieved:", len(jobs))

    # Step 2: Filter jobs by preferred titles
    matching_jobs = filter_jobs(jobs)

    print("\nMatching jobs:", len(matching_jobs))

    # Step 3: Display matching vacancies
    for job in matching_jobs:
        print("\n-----------------------------")
        print("Title:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Apply here:", job["url"])

except requests.exceptions.RequestException as error:
    print("Could not retrieve jobs:", error)