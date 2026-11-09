
import streamlit as st
import pandas as pd

from job_pipeline import run_job_search


# Page configuration
st.set_page_config(
    page_title="AI Job Search Dashboard",
    page_icon="🚀",
    layout="wide"
)


# Dashboard heading
st.title("🚀 AI Job Search Dashboard")

st.write(
    "Discover and rank Data Engineering "
    "and AI Automation opportunities in India."
)


# Run job search button
if st.button("🔍 Fetch Latest Jobs", type="primary"):

    with st.spinner("Fetching jobs and calculating match scores..."):

        try:
            results = run_job_search()

            st.session_state["job_results"] = results

        except Exception as error:
            st.error(f"Job search failed: {error}")


# Display results if available
if "job_results" in st.session_state:

    results = st.session_state["job_results"]

    ranked_jobs = results["ranked_jobs"]

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Jobs Fetched",
        results["total_jobs"]
    )

    col2.metric(
        "Potential Matches",
        results["potential_jobs"]
    )

    data_jobs = sum(
        "Data Engineering" in job.get("matched_tracks", [])
        for job in ranked_jobs
    )

    ai_jobs = sum(
        "AI Automation" in job.get("matched_tracks", [])
        for job in ranked_jobs
    )

    col3.metric("Data Engineering", data_jobs)
    col4.metric("AI Automation", ai_jobs)

    st.divider()

    # Company-wise job counts
    st.subheader("Jobs Retrieved by Company")

    company_data = pd.DataFrame(
        list(results["company_counts"].items()),
        columns=["Company", "Jobs"]
    )

    st.bar_chart(
        company_data,
        x="Company",
        y="Jobs"
    )

    # Career track distribution
    st.subheader("Jobs by Career Track")

    track_data = pd.DataFrame({
        "Career Track": [
            "Data Engineering",
            "AI Automation"
        ],
        "Jobs": [
            data_jobs,
            ai_jobs
        ]
    })

    st.bar_chart(
        track_data,
        x="Career Track",
        y="Jobs"
    )

    st.divider()

    # Ranked job listings
    st.subheader("🏆 Ranked Job Opportunities")

    for index, job in enumerate(ranked_jobs, start=1):

        with st.expander(
            f"#{index} | {job.get('title')} | "
            f"{job.get('company')} | "
            f"Score: {job.get('match_score')}/100"
        ):

            st.write("**Location:**", job.get("location"))

            st.write(
                "**Career Track:**",
                ", ".join(job.get("matched_tracks", []))
            )

            st.write(
                "**Matching Skills:**",
                ", ".join(job.get("matching_skills", []))
            )

            st.write(
                "**Missing / Not Confirmed Skills:**",
                ", ".join(job.get("not_confirmed", []))
            )

            st.write(
                "**Scoring Method:**",
                job.get("scoring_method")
            )

            st.link_button(
                "Apply for this Job",
                job.get("url")
            )

    # API errors
    if results["errors"]:

        st.warning("Some company APIs could not be accessed.")

        for error in results["errors"]:

            st.write(
                f"{error['company']}: {error['error']}"
            )

else:

    st.info(
        "Click 'Fetch Latest Jobs' to retrieve "
        "and rank current opportunities."
    )
