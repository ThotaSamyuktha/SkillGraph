// ==========================================
// SkillGraph - Main Cypher Queries
// ==========================================


// ==========================================
// 1. Get All Candidates
// ==========================================

MATCH (c:Candidate)
RETURN
    c.id AS id,
    c.name AS name,
    c.location AS location
ORDER BY c.name;


// ==========================================
// 2. Get Candidate Skills
// ==========================================

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)

RETURN
    s.id AS id,
    s.name AS name,
    s.category AS category
ORDER BY s.name;


// ==========================================
// 3. Direct Job Skill Matching
// ==========================================

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)

MATCH (j)-[:POSTED_BY]->(company:Company)
MATCH (j)-[:IN_CATEGORY]->(category:Category)

RETURN
    j.id AS job_id,
    j.title AS job_title,
    company.name AS company,
    category.name AS category,
    s.name AS matched_skill
ORDER BY j.title;


// ==========================================
// 4. Multi-Hop Related Skill Recommendation
// ==========================================
//
// Candidate
//    ↓ HAS_SKILL
// Skill
//    ↓ RELATED_TO
// Related Skill
//    ↓ REQUIRES
// Job
//

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      -[:RELATED_TO]->(related:Skill)
      <-[:REQUIRES]-(j:Job)

MATCH (j)-[:POSTED_BY]->(company:Company)

RETURN DISTINCT
    c.name AS candidate,
    s.name AS current_skill,
    related.name AS related_skill,
    j.title AS job,
    company.name AS company
ORDER BY j.title;


// ==========================================
// 5. Full Recommendation Path
// ==========================================
//
// Candidate → Skill → Related Skill → Job
//          → Company
//          → Category
//

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      -[:RELATED_TO]->(related:Skill)
      <-[:REQUIRES]-(j:Job)

MATCH (j)-[:POSTED_BY]->(company:Company)
MATCH (j)-[:IN_CATEGORY]->(category:Category)

RETURN DISTINCT
    c.name AS candidate,
    s.name AS current_skill,
    related.name AS related_skill,
    j.title AS job,
    company.name AS company,
    category.name AS category
ORDER BY j.title;


// ==========================================
// 6. Jobs Matching Multiple Candidate Skills
// ==========================================

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)

WITH
    j,
    collect(DISTINCT s.name) AS matched_skills

MATCH (j)-[:POSTED_BY]->(company:Company)

RETURN
    j.title AS job,
    company.name AS company,
    matched_skills,
    size(matched_skills) AS matched_skill_count
ORDER BY matched_skill_count DESC;


// ==========================================
// 7. Job Skill Requirements
// ==========================================

MATCH (j:Job {id: $job_id})
      -[:REQUIRES]->(s:Skill)

RETURN
    j.title AS job,
    collect(s.name) AS required_skills;


// ==========================================
// 8. Why Graph DB is Useful
// ==========================================
//
// This query connects a candidate to a job
// through multiple relationship types:
//
// Candidate
//    → HAS_SKILL
// Skill
//    → RELATED_TO
// Related Skill
//    → REQUIRES
// Job
//    → POSTED_BY
// Company
//
// The same relationship traversal would require
// multiple relational joins and relationship tables
// in a traditional relational database.
//

MATCH (c:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      -[:RELATED_TO]->(related:Skill)
      <-[:REQUIRES]-(j:Job)
      -[:POSTED_BY]->(company:Company)

RETURN DISTINCT
    c.name AS candidate,
    s.name AS existing_skill,
    related.name AS related_skill,
    j.title AS recommended_job,
    company.name AS company;