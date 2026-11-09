from job_search import filter_jobs

# Sample job listings (for testing only)
sample_jobs = [
    {
        "title": "AWS Data Engineer",
        "location": "Remote - India",
        "company": "Company A",
        "description": "Python, AWS, Snowflake and ETL",
        "url": "https://example.com/job1"
    },
    {
        "title": "React Frontend Developer",
        "location": "Bangalore, India",
        "company": "Company B",
        "description": "React and JavaScript",
        "url": "https://example.com/job2"
    },
    {
        "title": "Python Backend Developer",
        "location": "Remote",
        "company": "Company C",
        "description": "Python and FastAPI",
        "url": "https://example.com/job3"
    }
]

matching_jobs = filter_jobs(sample_jobs)

print("Matching Jobs:")
for job in matching_jobs:
    print(job["title"], "-", job["location"])
