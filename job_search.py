import requests

# Import preferences from config.py
from config import (
    ROLE_TITLE_KEYWORDS,
    EXCLUDED_TITLE_KEYWORDS,
    AI_DESCRIPTION_KEYWORDS
)


def fetch_greenhouse_jobs(company_token):

    url = (
        f"https://boards-api.greenhouse.io/"
        f"v1/boards/{company_token}/jobs"
    )

    params = {"content": "true"}

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):

        jobs.append({
            "job_id": job.get("id"),
            "title": job.get("title", ""),
            "company": company_token,
            "location": job.get("location", {}).get("name", ""),
            "description": job.get("content", ""),
            "url": job.get("absolute_url", "")
        })

    return jobs


def filter_jobs(jobs):

    matching_jobs = []
    seen_jobs = set()

    print("\nDEBUG: Searching across Data Engineering and AI Automation...")

    for job in jobs:

        title = job.get("title", "").lower()
        location = job.get("location", "").lower()
        description = job.get("description", "").lower()

        # 1. Exclude unwanted roles
        if any(word in title for word in EXCLUDED_TITLE_KEYWORDS):
            continue

        # 2. Check whether the title matches a career track
        matched_tracks = []

        for track, keywords in ROLE_TITLE_KEYWORDS.items():

            if not any(keyword in title for keyword in keywords):
                continue

            # 3. AI roles must also contain relevant description indicators
            if track == "AI Automation":

                has_ai_indicator = any(
                    keyword in description
                    for keyword in AI_DESCRIPTION_KEYWORDS
                )

                if not has_ai_indicator:
                    continue

            matched_tracks.append(track)

        # 4. Ignore jobs that don't match either career track
        if not matched_tracks:
            continue

        # 5. Accept only jobs explicitly listing India
        if "india" not in location:
            continue

        eligibility = "India location indicated"

        # 6. Avoid duplicate jobs
        job_key = (
            job.get("company", "").lower(),
            job.get("job_id") or job.get("url")
            or job.get("title", "") + "|" + location
        )

        if job_key in seen_jobs:
            continue

        seen_jobs.add(job_key)

        # 7. Preserve original job information
        job_copy = dict(job)

        job_copy["matched_tracks"] = matched_tracks
        job_copy["eligibility_status"] = eligibility

        matching_jobs.append(job_copy)

    # 8. Display summary
    print(f"\nTotal jobs fetched: {len(jobs)}")
    print(f"Potential matching jobs: {len(matching_jobs)}")

    for track in ROLE_TITLE_KEYWORDS:

        count = sum(
            track in job["matched_tracks"]
            for job in matching_jobs
        )

        print(f"{track}: {count} jobs")

    print("\nLocation eligibility breakdown:")
    print(f"India location indicated: {len(matching_jobs)}")

    return matching_jobs


if __name__ == "__main__":

    # Example: use a real Greenhouse board token
    company_token = "stripe"

    jobs = fetch_greenhouse_jobs(company_token)

    filtered_jobs = filter_jobs(jobs)

    print("Total jobs found:", len(jobs))

    print("Matching jobs:", len(filtered_jobs))

    for job in filtered_jobs:

        print("\nJob Title:", job["title"])
        print("Location:", job["location"])
        print("Application URL:", job["url"])
