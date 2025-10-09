-- =========================================
-- Drop tables if they exist
-- =========================================
DROP TABLE IF EXISTS research_trackr.research_projects CASCADE;
DROP TABLE IF EXISTS research_trackr.students CASCADE;
DROP TABLE IF EXISTS research_trackr.supervisors CASCADE;

-- =========================================
-- 1. Supervisors Table
-- =========================================
CREATE TABLE IF NOT EXISTS research_trackr.supervisors (
    supervisor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(10),
    specialization VARCHAR(100)
);

COPY research_trackr.supervisors(supervisor_id, name, title, specialization)
FROM 'C:\Program Files\PostgreSQL\18\pgAdmin 4\pg_data\ResearchTrackr\supervisors.csv'
WITH (
    FORMAT csv,
    DELIMITER ',',
    HEADER true,
    ENCODING 'UTF8',
    QUOTE '"',
    ESCAPE ''''
);

-- =========================================
-- 2. Students Table
-- =========================================
CREATE TABLE IF NOT EXISTS research_trackr.students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    year_of_study INT CHECK (year_of_study BETWEEN 2021 AND 2025),
    program VARCHAR(50)
);

COPY research_trackr.students(student_id, name, year_of_study, program)
FROM 'C:\Program Files\PostgreSQL\18\pgAdmin 4\pg_data\ResearchTrackr\students.csv'
WITH (
    FORMAT csv,
    DELIMITER ',',
    HEADER true,
    ENCODING 'UTF8',
    QUOTE '"',
    ESCAPE ''''
);

-- =========================================
-- 3. Research Projects Table
-- =========================================
CREATE TABLE IF NOT EXISTS research_trackr.research_projects (
    project_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES research_trackr.students(student_id) ON DELETE CASCADE,
    supervisor_id INT REFERENCES research_trackr.supervisors(supervisor_id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    category VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('Ongoing', 'Completed')),
    year_published INT CHECK (year_published BETWEEN 2021 AND 2025),
    dataset_available VARCHAR(3) CHECK (dataset_available IN ('Yes', 'No'))
);

COPY research_trackr.research_projects(project_id, student_id, supervisor_id, title, category, status, year_published, dataset_available)
FROM 'C:\Program Files\PostgreSQL\18\pgAdmin 4\pg_data\ResearchTrackr\research_projects.csv'
WITH (
    FORMAT csv,
    DELIMITER ',',
    HEADER true,
    ENCODING 'UTF8',
    QUOTE '"',
    ESCAPE ''''
);
