/* 1. Create tables*/

BEGIN TRANSACTION;

/* drop tables so they could be recreated*/

DROP INDEX IF EXISTS grades_values_index;

DROP TABLE IF EXISTS grades;

DROP INDEX IF EXISTS students_birth_year_index;

DROP INDEX IF EXISTS students_full_name_index;

DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name  TEXT    NOT NULL,
    birth_year INTEGER NOT NULL
                       CHECK (birth_year > 1800 AND
                              birth_year < 2026) 
);

CREATE INDEX IF NOT EXISTS students_full_name_index ON students (
    full_name
); --index for searching students full name

CREATE INDEX IF NOT EXISTS students_birth_year_index ON students (
    birth_year
); --index for searching students birth year

CREATE TABLE IF NOT EXISTS grades (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students (id), --foreign key to table students
    subject    TEXT    NOT NULL,
    grade      INTEGER NOT NULL
                       CHECK (grade >= 0 AND
                              grade <= 100) 
);

CREATE INDEX IF NOT EXISTS grades_values_index ON grades (
    grade
); --index for searching grades

COMMIT; 

/* 2. Insert data */

BEGIN TRANSACTION;

INSERT OR REPLACE INTO students (full_name, birth_year)
VALUES 
    ('Alice Johnson',2005),
    ('Brian Smith',2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006);
    
INSERT OR REPLACE INTO grades(student_id, subject, grade)
VALUES
    (1,'Math',88),
    (1,'English',92),
    (1,'Science',85),
    (2,'Math',75),
    (2,'History',83),
    (2,'English',79),
    (3,'Science',95),
    (3,'Math',91),
    (3,'Art',89),
    (4,'Math',84),
    (4,'Science',88),
    (4,'Physical Education',93),
    (5,'English',90),
    (5,'History',85),
    (5,'Math',88),
    (6,'Science',72),
    (6,'Math',78),
    (6,'English',81),
    (7,'Art',94),
    (7,'Science',87),
    (7,'Math',90),
    (8,'History',77),
    (8,'Math',83),
    (8,'Science',80),
    (9,'English',96),
    (9,'Math',89),
    (9,'Art',92);

COMMIT;

/* 3. Find all grades for specific student (Alice Johnson) */

SELECT grades.grade AS grade
FROM grades
       JOIN
       students ON grades.student_id = students.id
WHERE students.full_name = 'Alice Johnson';

/* 4. Calculate the average grade per student */

SELECT students.full_name AS student,
       avg(grades.grade) AS average_grade
  FROM grades
       JOIN
       students ON grades.student_id = students.id
 GROUP BY students.full_name;

/* 5. List all students born after 2004*/

SELECT students.full_name as full_name
  FROM students
 WHERE students.birth_year > 2004;

/* 6. Create a query that lists all subjects and their average grades */

SELECT grades.subject as subject,
       avg(grades.grade) as average_grade
  FROM grades
 GROUP BY grades.subject;

/* 7. Find the top 3 students with the highest average grades */

SELECT students.full_name AS student,
       avg(grades.grade) AS average_grade
  FROM grades
       JOIN
       students ON grades.student_id = students.id
 GROUP BY students.full_name
 ORDER BY avg(grade) DESC --sort by average grades from the biggest
 LIMIT 3; --top 3

 
/* 8. Show all students who have scored below 80 in any subject */

SELECT DISTINCT students.full_name,
                grades.subject,
                grades.grade
  FROM grades
       JOIN
       students ON grades.student_id = students.id
 WHERE grades.grade < 80;

