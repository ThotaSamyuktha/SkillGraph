# import os
# from flask import Flask, render_template, request
# from dotenv import load_dotenv
# from neo4j import GraphDatabase
# # ==========================================
# # Configuration
# # ==========================================

# load_dotenv()

# URI = os.getenv("COGNODB_URI")
# USERNAME = os.getenv("COGNODB_USERNAME")
# PASSWORD = os.getenv("COGNODB_PASSWORD")
# # ==========================================
# # Flask App
# # ==========================================

# import os

# from flask import Flask, render_template, request
# from dotenv import load_dotenv
# from neo4j import GraphDatabase


# # ==========================================
# # Configuration
# # ==========================================

# load_dotenv()

# URI = os.getenv("COGNODB_URI")
# USERNAME = os.getenv("COGNODB_USERNAME")
# PASSWORD = os.getenv("COGNODB_PASSWORD")


# # ==========================================
# # Flask App
# # ==========================================

# app = Flask(__name__)


# # ==========================================
# # CognoDB Connection
# # ==========================================

# driver = GraphDatabase.driver(
#     URI,
#     auth=(USERNAME, PASSWORD)
# )


# # ==========================================
# # Database Queries
# # ==========================================

# def get_candidates():

#     query = """
#     MATCH (c:Candidate)
#     RETURN c.id AS id,
#            c.name AS name,
#            c.location AS location
#     ORDER BY c.name
#     """

#     with driver.session() as session:

#         result = session.run(query)

#         return [record.data() for record in result]


# def get_candidate_skills(candidate_id):

#     query = """
#     MATCH (c:Candidate {id: $candidate_id})
#           -[:HAS_SKILL]->(s:Skill)

#     RETURN s.id AS id,
#            s.name AS name,
#            s.category AS category

#     ORDER BY s.name
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             candidate_id=candidate_id
#         )

#         return [record.data() for record in result]
# def get_skill_match_analysis(candidate_id, job_id):

#     query = """
#     MATCH (c:Candidate {id: $candidate_id})
#           -[:HAS_SKILL]->(candidate_skill:Skill)

#     MATCH (j:Job {id: $job_id})
#           -[:REQUIRES]->(required_skill:Skill)

#     OPTIONAL MATCH (candidate_skill)-[:RELATED_TO]->(required_skill)

#     WITH
#         required_skill,
#         collect(DISTINCT candidate_skill.name) AS candidate_skills

#     RETURN
#         required_skill.name AS required_skill,
#         candidate_skills
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             candidate_id=candidate_id,
#             job_id=job_id
#         )

#         rows = [record.data() for record in result]

#     direct_skills = []
#     related_skills = []
#     missing_skills = []

#     for row in rows:

#         required_skill = row["required_skill"]
#         candidate_skills = row["candidate_skills"]

#         if required_skill in candidate_skills:

#             direct_skills.append(required_skill)

#         else:

#             # Check whether this required skill is related
#             # to any skill the candidate already has.

#             related_query = """
#             MATCH (c:Candidate {id: $candidate_id})
#                   -[:HAS_SKILL]->(candidate_skill:Skill)
#                   -[:RELATED_TO]->(required_skill:Skill)

#             WHERE required_skill.name = $required_skill

#             RETURN required_skill.name AS skill
#             """

#             related_result = session.run(
#                 related_query,
#                 candidate_id=candidate_id,
#                 required_skill=required_skill
#             )

#             related_record = related_result.single()

#             if related_record:
#                 related_skills.append(required_skill)
#             else:
#                 missing_skills.append(required_skill)

#     total_required = (
#         len(direct_skills)
#         + len(related_skills)
#         + len(missing_skills)
#     )

#     if total_required > 0:

#         weighted_score = (
#             len(direct_skills) * 1.0
#             + len(related_skills) * 0.5
#         )

#         match_percentage = round(
#             (weighted_score / total_required) * 100
#         )

#     else:

#         match_percentage = 0

#     return {
#         "direct_skills": direct_skills,
#         "related_skills": related_skills,
#         "missing_skills": missing_skills,
#         "match_percentage": match_percentage
#     }
# def get_job_recommendations(candidate_id):

#     query = """
#     MATCH (c:Candidate {id: $candidate_id})
#           -[:HAS_SKILL]->(candidate_skill:Skill)

#     OPTIONAL MATCH (candidate_skill)-[:RELATED_TO]->(related_skill:Skill)

#     MATCH (j:Job)
#           -[:REQUIRES]->(required_skill:Skill)

#     MATCH (j)-[:POSTED_BY]->(company:Company)

#     MATCH (j)-[:IN_CATEGORY]->(category:Category)

#     WHERE required_skill = candidate_skill
#        OR required_skill = related_skill

#     WITH
#         j,
#         company,
#         category,

#         collect(
#             DISTINCT CASE
#                 WHEN required_skill = candidate_skill
#                 THEN required_skill.name
#             END
#         ) AS direct_matches,

#         collect(
#             DISTINCT CASE
#                 WHEN required_skill = related_skill
#                 THEN required_skill.name
#             END
#         ) AS related_matches

#     WITH
#         j,
#         company,
#         category,

#         [x IN direct_matches WHERE x IS NOT NULL]
#             AS direct_skills,

#         [x IN related_matches WHERE x IS NOT NULL]
#             AS related_skills

#     RETURN
#         j.id AS id,
#         j.title AS title,
#         j.location AS location,
#         j.experience AS experience,
#         j.salary AS salary,
#         company.name AS company,
#         category.name AS category,

#         direct_skills,
#         related_skills,

#         CASE
#             WHEN size(direct_skills) > 0
#                  AND size(related_skills) > 0
#             THEN "Direct + Related"

#             WHEN size(direct_skills) > 0
#             THEN "Direct"

#             ELSE "Related Skill"
#         END AS match_type

#     ORDER BY title
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             candidate_id=candidate_id
#         )

#         return [record.data() for record in result]
# def get_job_details(job_id):

#     query = """
#     MATCH (j:Job {id: $job_id})
#           -[:POSTED_BY]->(company:Company)

#     MATCH (j)-[:IN_CATEGORY]->(category:Category)

#     RETURN j.id AS id,
#            j.title AS title,
#            j.location AS location,
#            j.experience AS experience,
#            j.salary AS salary,
#            company.name AS company,
#            category.name AS category
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             job_id=job_id
#         )

#         record = result.single()

#         if record:
#             return record.data()

#         return None


# def get_job_required_skills(job_id):

#     query = """
#     MATCH (j:Job {id: $job_id})
#           -[:REQUIRES]->(s:Skill)

#     RETURN s.name AS name

#     ORDER BY s.name
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             job_id=job_id
#         )

#         return [record["name"] for record in result]


# def get_candidate_skill_names(candidate_id):

#     query = """
#     MATCH (c:Candidate {id: $candidate_id})
#           -[:HAS_SKILL]->(s:Skill)

#     RETURN s.name AS name

#     ORDER BY s.name
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             candidate_id=candidate_id
#         )

#         return [record["name"] for record in result]

# def get_related_candidate_skills(candidate_id):

#     query = """
#     MATCH (c:Candidate {id: $candidate_id})
#           -[:HAS_SKILL]->(candidate_skill:Skill)
#           -[:RELATED_TO]->(related_skill:Skill)

#     RETURN DISTINCT related_skill.name AS name
#     ORDER BY related_skill.name
#     """

#     with driver.session() as session:

#         result = session.run(
#             query,
#             candidate_id=candidate_id
#         )

#         return [record["name"] for record in result]
# # ==========================================
# # Routes
# # ==========================================

# @app.route("/")
# def home():

#     try:

#         candidates = get_candidates()

#         return render_template(
#             "index.html",
#             candidates=candidates
#         )

#     except Exception as e:

#         print("Database error:", e)

#         return render_template(
#             "index.html",
#             candidates=[],
#             error="Unable to connect to the database."
#         )
# @app.route("/job/<job_id>")
# def job_details(job_id):

#     candidate_id = request.args.get("candidate_id")

#     try:

#         job = get_job_details(job_id)

#         if not job:
#             return render_template(
#                 "job_details.html",
#                 job=None,
#                 error="Job not found."
#             )

#         # Get candidate information
#         candidates = get_candidates()

#         candidate = next(
#             (
#                 c for c in candidates
#                 if c["id"] == candidate_id
#             ),
#             None
#         )

#         if not candidate:
#             return render_template(
#                 "job_details.html",
#                 job=job,
#                 candidate=None,
#                 error="Candidate not found."
#             )

#         # Graph-based skill analysis
#         analysis = get_skill_match_analysis(
#             candidate_id,
#             job_id
#         )

#         return render_template(
#             "job_details.html",
#             job=job,
#             candidate=candidate,
#             matched_skills=analysis["direct_skills"],
#             related_skills=analysis["related_skills"],
#             missing_skills=analysis["missing_skills"],
#             match_percentage=analysis["match_percentage"]
#         )

#     except Exception as e:

#         print("Job details error:", e)

#         return render_template(
#             "job_details.html",
#             job=None,
#             candidate=None,
#             error="Unable to load job details. Please try again."
#         )

# # ==========================================
# # Job Details Route
# # ==========================================


# # ==========================================
# # Application Entry Point
# # ==========================================

# if __name__ == "__main__":

#     app.run(
#         debug=True,
#         host="127.0.0.1",
#         port=5000
#     )

import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
from neo4j import GraphDatabase


# ==========================================
# Configuration
# ==========================================

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)


# ==========================================
# CognoDB Connection
# ==========================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# ==========================================
# Database Queries
# ==========================================

def get_candidates():

    query = """
    MATCH (c:Candidate)

    RETURN
        c.id AS id,
        c.name AS name,
        c.location AS location

    ORDER BY c.name
    """

    with driver.session() as session:

        result = session.run(query)

        return [record.data() for record in result]


def get_candidate_skills(candidate_id):

    query = """
    MATCH (c:Candidate {id: $candidate_id})
          -[:HAS_SKILL]->(s:Skill)

    RETURN
        s.id AS id,
        s.name AS name,
        s.category AS category

    ORDER BY s.name
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_id=candidate_id
        )

        return [record.data() for record in result]


def get_candidate_skill_names(candidate_id):

    query = """
    MATCH (c:Candidate {id: $candidate_id})
          -[:HAS_SKILL]->(s:Skill)

    RETURN s.name AS name

    ORDER BY s.name
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_id=candidate_id
        )

        return [record["name"] for record in result]


def get_related_candidate_skills(candidate_id):

    query = """
    MATCH (c:Candidate {id: $candidate_id})
          -[:HAS_SKILL]->(candidate_skill:Skill)
          -[:RELATED_TO]->(related_skill:Skill)

    RETURN DISTINCT related_skill.name AS name

    ORDER BY related_skill.name
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_id=candidate_id
        )

        return [record["name"] for record in result]


# ==========================================
# Graph-Based Skill Match Analysis
# ==========================================

def get_skill_match_analysis(candidate_id, job_id):

    query = """
    MATCH (c:Candidate {id: $candidate_id})
          -[:HAS_SKILL]->(candidate_skill:Skill)

    MATCH (j:Job {id: $job_id})
          -[:REQUIRES]->(required_skill:Skill)

    OPTIONAL MATCH
        (candidate_skill)-[:RELATED_TO]->(related_required_skill:Skill)

    WITH
        required_skill,
        collect(DISTINCT candidate_skill.name) AS candidate_skills,
        collect(DISTINCT related_required_skill.name)
            AS related_skill_names

    RETURN
        required_skill.name AS required_skill,
        candidate_skills,
        related_skill_names
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_id=candidate_id,
            job_id=job_id
        )

        rows = [record.data() for record in result]

        direct_skills = []
        related_skills = []
        missing_skills = []

        for row in rows:

            required_skill = row["required_skill"]

            candidate_skills = row["candidate_skills"]

            related_skill_names = row["related_skill_names"]

            # Direct match
            if required_skill in candidate_skills:

                direct_skills.append(required_skill)

            # Related match
            elif required_skill in related_skill_names:

                related_skills.append(required_skill)

            # Missing skill
            else:

                missing_skills.append(required_skill)

    total_required = (
        len(direct_skills)
        + len(related_skills)
        + len(missing_skills)
    )

    if total_required > 0:

        weighted_score = (
            len(direct_skills) * 1.0
            + len(related_skills) * 0.5
        )

        match_percentage = round(
            (weighted_score / total_required) * 100
        )

    else:

        match_percentage = 0

    if match_percentage >= 80:

        match_label = "Excellent Match"

    elif match_percentage >= 50:

        match_label = "Good Match"

    elif match_percentage > 0:

        match_label = "Partial Match"

    else:

        match_label = "Low Match"

    return {
        "direct_skills": direct_skills,
        "related_skills": related_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "match_label": match_label
    }


# ==========================================
# Job Recommendations
# ==========================================

def get_job_recommendations(candidate_id):

    query = """
    MATCH (c:Candidate {id: $candidate_id})
          -[:HAS_SKILL]->(candidate_skill:Skill)

    OPTIONAL MATCH
        (candidate_skill)-[:RELATED_TO]->(related_skill:Skill)

    MATCH (j:Job)
          -[:REQUIRES]->(required_skill:Skill)

    MATCH (j)-[:POSTED_BY]->(company:Company)

    MATCH (j)-[:IN_CATEGORY]->(category:Category)

    WHERE required_skill = candidate_skill
       OR required_skill = related_skill

    WITH
        j,
        company,
        category,

        collect(
            DISTINCT CASE
                WHEN required_skill = candidate_skill
                THEN required_skill.name
            END
        ) AS direct_matches,

        collect(
            DISTINCT CASE
                WHEN required_skill = related_skill
                THEN required_skill.name
            END
        ) AS related_matches

    WITH
        j,
        company,
        category,

        [x IN direct_matches
         WHERE x IS NOT NULL] AS direct_skills,

        [x IN related_matches
         WHERE x IS NOT NULL] AS related_skills

    RETURN
        j.id AS id,
        j.title AS title,
        j.location AS location,
        j.experience AS experience,
        j.salary AS salary,
        company.name AS company,
        category.name AS category,

        direct_skills,
        related_skills,

        CASE

            WHEN size(direct_skills) > 0
                 AND size(related_skills) > 0

            THEN "Direct + Related"

            WHEN size(direct_skills) > 0

            THEN "Direct"

            ELSE "Related Skill"

        END AS match_type

    ORDER BY title
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_id=candidate_id
        )

        return [record.data() for record in result]


# ==========================================
# Job Details
# ==========================================

def get_job_details(job_id):

    query = """
    MATCH (j:Job {id: $job_id})
          -[:POSTED_BY]->(company:Company)

    MATCH (j)-[:IN_CATEGORY]->(category:Category)

    RETURN
        j.id AS id,
        j.title AS title,
        j.location AS location,
        j.experience AS experience,
        j.salary AS salary,
        company.name AS company,
        category.name AS category
    """

    with driver.session() as session:

        result = session.run(
            query,
            job_id=job_id
        )

        record = result.single()

        if record:

            return record.data()

        return None


def get_job_required_skills(job_id):

    query = """
    MATCH (j:Job {id: $job_id})
          -[:REQUIRES]->(s:Skill)

    RETURN s.name AS name

    ORDER BY s.name
    """

    with driver.session() as session:

        result = session.run(
            query,
            job_id=job_id
        )

        return [record["name"] for record in result]


# ==========================================
# Routes
# ==========================================

@app.route("/")
def home():

    try:

        candidates = get_candidates()

        return render_template(
            "index.html",
            candidates=candidates
        )

    except Exception as e:

        print("Database error:", e)

        return render_template(
            "index.html",
            candidates=[],
            error="Unable to connect to the database."
        )


# ==========================================
# Jobs / Recommendations Route
# ==========================================

@app.route("/jobs")
def jobs():

    candidate_id = request.args.get("candidate_id")

    try:

        candidates = get_candidates()

        candidate = next(
            (
                c for c in candidates
                if c["id"] == candidate_id
            ),
            None
        )

        if not candidate:

            return render_template(
                "jobs.html",
                candidate=None,
                skills=[],
                jobs=[],
                error="Candidate not found."
            )

        skills = get_candidate_skills(candidate_id)

        jobs = get_job_recommendations(candidate_id)

        return render_template(
            "jobs.html",
            candidate=candidate,
            skills=skills,
            jobs=jobs
        )

    except Exception as e:

        print("Jobs page error:", e)

        return render_template(
            "jobs.html",
            candidate=None,
            skills=[],
            jobs=[],
            error="Unable to load job recommendations. Please try again."
        )


# ==========================================
# Individual Job Details Route
# ==========================================

@app.route("/job/<job_id>")
def job_details(job_id):

    candidate_id = request.args.get("candidate_id")

    try:

        job = get_job_details(job_id)

        if not job:

            return render_template(
                "job_details.html",
                job=None,
                candidate=None,
                matched_skills=[],
                related_skills=[],
                missing_skills=[],
                match_percentage=0,
                match_label="Low Match",
                error="Job not found."
            )

        candidates = get_candidates()

        candidate = next(
            (
                c for c in candidates
                if c["id"] == candidate_id
            ),
            None
        )

        if not candidate:

            return render_template(
                "job_details.html",
                job=job,
                candidate=None,
                matched_skills=[],
                related_skills=[],
                missing_skills=[],
                match_percentage=0,
                match_label="Low Match",
                error="Candidate not found."
            )

        # Graph-based skill analysis
        analysis = get_skill_match_analysis(
            candidate_id,
            job_id
        )

        return render_template(
            "job_details.html",
            job=job,
            candidate=candidate,

            matched_skills=analysis["direct_skills"],

            related_skills=analysis["related_skills"],

            missing_skills=analysis["missing_skills"],

            match_percentage=analysis["match_percentage"],

            match_label=analysis["match_label"]
        )

    except Exception as e:

        print("Job details error:", e)

        return render_template(
            "job_details.html",
            job=None,
            candidate=None,
            matched_skills=[],
            related_skills=[],
            missing_skills=[],
            match_percentage=0,
            match_label="Low Match",
            error="Unable to load job details. Please try again."
        )


# ==========================================
# Application Entry Point
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )