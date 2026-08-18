import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


# Connect to CognoDB
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def clear_database(tx):
    tx.run("""
        MATCH (n)
        DETACH DELETE n
    """).consume()


def create_data(tx):

    # ==========================================
    # CATEGORIES
    # ==========================================

    categories = [
        ("CAT001", "Software Development"),
        ("CAT002", "Data Engineering"),
        ("CAT003", "Cloud Computing"),
        ("CAT004", "Machine Learning")
    ]

    for category_id, name in categories:
        tx.run("""
            MERGE (c:Category {id: $id})
            SET c.name = $name
        """,
        id=category_id,
        name=name).consume()


    # ==========================================
    # COMPANIES
    # ==========================================

    companies = [
        ("CO001", "TechNova Solutions", "Hyderabad"),
        ("CO002", "DataFlow Technologies", "Bangalore"),
        ("CO003", "CloudWorks India", "Pune"),
        ("CO004", "FinTech Labs", "Mumbai"),
        ("CO005", "AI Solutions Pvt Ltd", "Hyderabad"),
        ("CO006", "CodeCraft Technologies", "Chennai"),
        ("CO007", "NextGen Systems", "Bangalore"),
        ("CO008", "InnovateTech", "Pune")
    ]

    for company_id, name, location in companies:
        tx.run("""
            MERGE (c:Company {id: $id})
            SET c.name = $name,
                c.location = $location
        """,
        id=company_id,
        name=name,
        location=location).consume()


    # ==========================================
    # SKILLS
    # ==========================================

    skills = [
        ("S001", "Python", "Programming"),
        ("S002", "SQL", "Database"),
        ("S003", "Flask", "Backend"),
        ("S004", "Django", "Backend"),
        ("S005", "FastAPI", "Backend"),
        ("S006", "PySpark", "Data Engineering"),
        ("S007", "Apache Spark", "Data Engineering"),
        ("S008", "AWS", "Cloud"),
        ("S009", "Azure", "Cloud"),
        ("S010", "Docker", "DevOps"),
        ("S011", "Kubernetes", "DevOps"),
        ("S012", "Git", "Tools"),
        ("S013", "Linux", "Operating System"),
        ("S014", "MongoDB", "Database"),
        ("S015", "Machine Learning", "AI")
    ]

    for skill_id, name, category in skills:
        tx.run("""
            MERGE (s:Skill {id: $id})
            SET s.name = $name,
                s.category = $category
        """,
        id=skill_id,
        name=name,
        category=category).consume()


    # ==========================================
    # SKILL RELATIONSHIPS
    # ==========================================

    skill_relationships = [
        ("S001", "S006"),  # Python -> PySpark
        ("S006", "S007"),  # PySpark -> Apache Spark
        ("S001", "S003"),  # Python -> Flask
        ("S001", "S004"),  # Python -> Django
        ("S001", "S005"),  # Python -> FastAPI
        ("S008", "S010"),  # AWS -> Docker
        ("S009", "S010"),  # Azure -> Docker
        ("S010", "S011"),  # Docker -> Kubernetes
        ("S012", "S013"),  # Git -> Linux
        ("S002", "S006"),  # SQL -> PySpark
        ("S014", "S002"),  # MongoDB -> SQL
        ("S015", "S001")   # ML -> Python
    ]

    for skill1, skill2 in skill_relationships:
        tx.run("""
            MATCH (s1:Skill {id: $skill1})
            MATCH (s2:Skill {id: $skill2})
            MERGE (s1)-[:RELATED_TO]->(s2)
        """,
        skill1=skill1,
        skill2=skill2).consume()


    # ==========================================
    # CANDIDATES
    # ==========================================

    candidates = [
        ("C001", "Samyuktha", "sam@example.com", "Hyderabad"),
        ("C002", "Rahul", "rahul@example.com", "Bangalore"),
        ("C003", "Priya", "priya@example.com", "Chennai"),
        ("C004", "Arjun", "arjun@example.com", "Pune"),
        ("C005", "Sneha", "sneha@example.com", "Mumbai")
    ]

    for candidate_id, name, email, location in candidates:
        tx.run("""
            MERGE (c:Candidate {id: $id})
            SET c.name = $name,
                c.email = $email,
                c.location = $location
        """,
        id=candidate_id,
        name=name,
        email=email,
        location=location).consume()


    # ==========================================
    # CANDIDATE SKILLS
    # ==========================================

    candidate_skills = [
        ("C001", "S001"),  # Samyuktha - Python
        ("C001", "S002"),  # Samyuktha - SQL
        ("C001", "S003"),  # Samyuktha - Flask
        ("C001", "S012"),  # Samyuktha - Git

        ("C002", "S001"),  # Rahul - Python
        ("C002", "S004"),  # Rahul - Django
        ("C002", "S012"),  # Rahul - Git

        ("C003", "S002"),  # Priya - SQL
        ("C003", "S006"),  # Priya - PySpark
        ("C003", "S007"),  # Priya - Spark

        ("C004", "S008"),  # Arjun - AWS
        ("C004", "S010"),  # Arjun - Docker
        ("C004", "S011"),  # Arjun - Kubernetes

        ("C005", "S001"),  # Sneha - Python
        ("C005", "S015"),  # Sneha - Machine Learning
        ("C005", "S002")   # Sneha - SQL
    ]

    for candidate_id, skill_id in candidate_skills:
        tx.run("""
            MATCH (c:Candidate {id: $candidate_id})
            MATCH (s:Skill {id: $skill_id})
            MERGE (c)-[:HAS_SKILL]->(s)
        """,
        candidate_id=candidate_id,
        skill_id=skill_id).consume()


    # ==========================================
    # JOBS
    # ==========================================

    jobs = [
        ("J001", "Python Developer", "Hyderabad", "Fresher", "4-7 LPA", "CO001", "CAT001"),
        ("J002", "Backend Developer", "Bangalore", "0-2 Years", "5-8 LPA", "CO006", "CAT001"),
        ("J003", "Junior Python Developer", "Pune", "Fresher", "3-6 LPA", "CO008", "CAT001"),
        ("J004", "Data Engineer", "Bangalore", "0-2 Years", "6-10 LPA", "CO002", "CAT002"),
        ("J005", "Junior Data Engineer", "Hyderabad", "Fresher", "4-7 LPA", "CO002", "CAT002"),
        ("J006", "Big Data Developer", "Chennai", "1-3 Years", "6-11 LPA", "CO007", "CAT002"),
        ("J007", "Cloud Engineer", "Pune", "0-2 Years", "5-9 LPA", "CO003", "CAT003"),
        ("J008", "AWS Cloud Associate", "Bangalore", "Fresher", "4-7 LPA", "CO003", "CAT003"),
        ("J009", "DevOps Engineer", "Hyderabad", "1-3 Years", "6-10 LPA", "CO007", "CAT003"),
        ("J010", "Machine Learning Engineer", "Hyderabad", "0-2 Years", "6-12 LPA", "CO005", "CAT004"),
        ("J011", "Junior ML Engineer", "Mumbai", "Fresher", "4-8 LPA", "CO005", "CAT004"),
        ("J012", "Software Engineer", "Chennai", "0-2 Years", "5-9 LPA", "CO006", "CAT001"),
        ("J013", "Full Stack Developer", "Bangalore", "0-2 Years", "5-9 LPA", "CO001", "CAT001"),
        ("J014", "Data Platform Engineer", "Pune", "1-3 Years", "7-12 LPA", "CO002", "CAT002"),
        ("J015", "Cloud Software Engineer", "Mumbai", "0-2 Years", "6-10 LPA", "CO003", "CAT003")
    ]

    for job_id, title, location, experience, salary, company_id, category_id in jobs:

        tx.run("""
            MERGE (j:Job {id: $job_id})
            SET j.title = $title,
                j.location = $location,
                j.experience = $experience,
                j.salary = $salary

            WITH j

            MATCH (c:Company {id: $company_id})
            MATCH (cat:Category {id: $category_id})

            MERGE (j)-[:POSTED_BY]->(c)
            MERGE (j)-[:IN_CATEGORY]->(cat)
        """,
        job_id=job_id,
        title=title,
        location=location,
        experience=experience,
        salary=salary,
        company_id=company_id,
        category_id=category_id).consume()


    # ==========================================
    # JOB REQUIRED SKILLS
    # ==========================================

    job_skills = [

        # Python Developer
        ("J001", "S001"),
        ("J001", "S002"),
        ("J001", "S003"),
        ("J001", "S012"),

        # Backend Developer
        ("J002", "S001"),
        ("J002", "S004"),
        ("J002", "S012"),

        # Junior Python Developer
        ("J003", "S001"),
        ("J003", "S005"),
        ("J003", "S012"),

        # Data Engineer
        ("J004", "S001"),
        ("J004", "S002"),
        ("J004", "S006"),
        ("J004", "S008"),

        # Junior Data Engineer
        ("J005", "S001"),
        ("J005", "S002"),
        ("J005", "S006"),

        # Big Data Developer
        ("J006", "S006"),
        ("J006", "S007"),
        ("J006", "S002"),

        # Cloud Engineer
        ("J007", "S008"),
        ("J007", "S010"),
        ("J007", "S012"),

        # AWS Cloud Associate
        ("J008", "S008"),
        ("J008", "S010"),

        # DevOps Engineer
        ("J009", "S008"),
        ("J009", "S010"),
        ("J009", "S011"),
        ("J009", "S013"),

        # Machine Learning Engineer
        ("J010", "S001"),
        ("J010", "S002"),
        ("J010", "S015"),

        # Junior ML Engineer
        ("J011", "S001"),
        ("J011", "S015"),

        # Software Engineer
        ("J012", "S001"),
        ("J012", "S002"),
        ("J012", "S012"),

        # Full Stack Developer
        ("J013", "S001"),
        ("J013", "S003"),
        ("J013", "S002"),

        # Data Platform Engineer
        ("J014", "S002"),
        ("J014", "S006"),
        ("J014", "S007"),
        ("J014", "S010"),

        # Cloud Software Engineer
        ("J015", "S001"),
        ("J015", "S008"),
        ("J015", "S010")
    ]

    for job_id, skill_id in job_skills:
        tx.run("""
            MATCH (j:Job {id: $job_id})
            MATCH (s:Skill {id: $skill_id})
            MERGE (j)-[:REQUIRES]->(s)
        """,
        job_id=job_id,
        skill_id=skill_id).consume()


def main():

    try:
        driver.verify_connectivity()
        print("Connected to CognoDB!")

        with driver.session() as session:

            print("Clearing old test data...")
            session.execute_write(clear_database)

            print("Creating SkillGraph data...")
            session.execute_write(create_data)

        print()
        print("===================================")
        print("SkillGraph seed completed!")
        print("===================================")
        print("5 Candidates")
        print("15 Skills")
        print("8 Companies")
        print("15 Jobs")
        print("4 Categories")
        print("Relationships created successfully!")

    except Exception as e:
        print("ERROR:", e)

    finally:
        driver.close()


if __name__ == "__main__":
    main()