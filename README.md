# SkillGraph – Intelligent Job & Skill Recommendation System

SkillGraph is a graph-based job recommendation application built with Flask and CognoDB.

The application connects candidates, skills, jobs, companies, and job categories using graph relationships. It recommends relevant jobs based on both direct skills and related skills.

---

## Problem Statement

Traditional job recommendation systems often compare candidate skills with job requirements using simple lists or relational joins.

SkillGraph uses a graph database to model the relationships between:

- Candidates
- Skills
- Related Skills
- Jobs
- Companies
- Categories

This allows the application to discover job opportunities through connected skill paths.

---

## Why a Graph Database?

A graph database is useful for SkillGraph because the recommendation depends on relationships between entities.

For example:

Candidate → HAS_SKILL → Python
           ↓
        RELATED_TO
           ↓
        PySpark
           ↓
        REQUIRED_BY
           ↓
        Data Engineer
           ↓
        POSTED_BY
           ↓
        DataFlow Technologies

This type of multi-hop relationship traversal is natural in a graph database.

In a relational database, the same recommendation would require multiple tables and JOIN operations to represent and traverse these relationships.

---

## Graph Data Model

### Nodes

| Node | Properties |
|---|---|
| Candidate | id, name, email, location |
| Skill | id, name, category |
| Job | id, title, location, experience, salary |
| Company | id, name, location |
| Category | id, name |

### Relationships

| Relationship | Description |
|---|---|
| HAS_SKILL | Candidate possesses a skill |
| RELATED_TO | One skill is related to another skill |
| REQUIRES | Job requires a skill |
| POSTED_BY | Job is posted by a company |
| IN_CATEGORY | Job belongs to a category |

### Graph Structure

```text
Candidate
    |
 HAS_SKILL
    |
    v
  Skill
    |
RELATED_TO
    |
    v
  Skill
    |
 REQUIRES
    |
    v
   Job
   / \
  /   \
POSTED  IN_CATEGORY
 /        \
v          v
Company   Category