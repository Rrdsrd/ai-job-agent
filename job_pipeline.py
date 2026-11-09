
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
    "yipitdata",
    "globalizationpartners"
]


def run_job_search():

    all_jobs = []
    company_counts = {}
    errors = []

    # 1. Fetch jobs from all companies
    for company in COMPANIES:

        try:
            jobs = fetch_greenhouse_jobs(company)

            all_jobs.extend(jobs)

            company_counts[company] = len(jobs)

        except Exception as error:

            errors.append({
                "company": company,
                "error": str(error)
            })

    # 2. Filter relevant jobs
    potential_jobs = filter_jobs(all_jobs)

    # 3. Rank matching jobs
    ranked_jobs = rank_jobs(potential_jobs)

    # 4. Return results for Streamlit
    return {
        "total_jobs": len(all_jobs),
        "potential_jobs": len(potential_jobs),
        "company_counts": company_counts,
        "ranked_jobs": ranked_jobs,
        "errors": errors
    }
