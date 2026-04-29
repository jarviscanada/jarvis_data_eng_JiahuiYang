# Introduction
SQL (Structured Query Language) is a fundamental tool for working with relational databases. It is widely used by developers, data engineers, and data analysts to store, retrieve, and manipulate data efficiently.

This project is a hands-on learning exercise designed to build practical SQL skills using a PostgreSQL database. The dataset simulates a club management system and includes three main tables:

- **cd.members** : stores member information
- **cd.facilities** : stores facility details
- **cd.bookings** : stores booking records

This project uses a PostgreSQL instance running in a Docker container. By working through real SQL queries, this project helps strengthen understanding of:

- Data retrieval (`SELECT`)
- Filtering (`WHERE`, `HAVING`)
- Joins and relationships (Primary Key, Foreign Key)
- Aggregations (`GROUP BY`)
- Subqueries and window functions

# SQL Queries
This section contains solutions to SQL exercises performed on the `cd` schema.
## Table Setup
The following SQL script creates the schema and tables used for the exercise.
```sql
CREATE DATABASE exercises;
CREATE SCHEMA cd;

CREATE TABLE bookings (
    bookid integer NOT NULL,
    facid integer NOT NULL,
    memid integer NOT NULL,
    starttime timestamp without time zone NOT NULL,
    slots integer NOT NULL
);


CREATE TABLE facilities (
    facid integer NOT NULL,
    name character varying(100) NOT NULL,
    membercost numeric NOT NULL,
    guestcost numeric NOT NULL,
    initialoutlay numeric NOT NULL,
    monthlymaintenance numeric NOT NULL
);


CREATE TABLE members (
    memid integer NOT NULL,
    surname character varying(200) NOT NULL,
    firstname character varying(200) NOT NULL,
    address character varying(300) NOT NULL,
    zipcode integer NOT NULL,
    telephone character varying(20) NOT NULL,
    recommendedby integer,
    joindate timestamp without time zone NOT NULL
);
```
## Practice question solutions
```sql
-- Q1
INSERT INTO cd.facilities(
    facid, name, membercost, guestcost,
    initialoutlay, monthlymaintenance
)
VALUES
    (9, 'Spa', '20', '30', 100000, 800);

-- Q2
INSERT INTO cd.facilities (
    facid, name, membercost, guestcost,
    initialoutlay, monthlymaintenance
)
VALUES
    (
        (
            SELECT
                MAX(facid) + 1
            FROM
                cd.facilities
        ),
        'Spa',
        20,
        30,
        100000,
        800
    );

-- Q3
UPDATE cd.facilities
SET initialoutlay = 10000
WHERE name = 'Tennis Court 2';

-- Q4
UPDATE cd.facilities
SET
    membercost = (SELECT membercost*1.1 FROM cd.facilities WHERE name = 'Tennis Court 1'),
    guestcost = (SELECT guestcost*1.1 FROM cd.facilities WHERE name = 'Tennis Court 1')
WHERE name = 'Tennis Court 2';

-- Q5
DELETE FROM cd.bookings;

-- Q6
DELETE FROM cd.members
WHERE memid = 37;

-- Q7
SELECT
    facid, name, membercost, monthlymaintenance
FROM
    cd.facilities
WHERE
    membercost >0 AND (membercost < monthlymaintenance * 0.02);

-- Q8
SELECT
    *
FROM
    cd.facilities
WHERE
    name LIKE '%Tennis%';

-- Q9
SELECT
    *
FROM
    cd.facilities
WHERE
    facid in (1,5);

-- Q10
SELECT
    memid, surname, firstname, joindate
FROM
    cd.members
WHERE
    joindate >= '2012-09-01';

-- Q11
SELECT
    surname
FROM
    cd.members
UNION
SELECT
    name
FROM
    cd.facilities;

-- Q12
SELECT
    b.starttime
FROM
    cd.bookings b
        JOIN cd.members m ON m.memid = b.memid
WHERE
    m.firstname = 'David'
  AND m.surname = 'Farrell';

-- Q13
SELECT
    b.starttime AS start,
    f.name AS name
FROM
    cd.bookings b
        JOIN cd.facilities f ON f.facid = b.facid
WHERE
    f.name in (
               'Tennis Court 1', 'Tennis Court 2'
        )
  AND b.starttime >= '2012-09-21'
  AND b.starttime < '2012-09-22'
ORDER BY
    start;

-- Q14
SELECT
    m1.firstname AS memfname,
    m1.surname AS memsname,
    m2.firstname AS recfname,
    m2.surname AS recsname
FROM
    cd.members m1
        LEFT JOIN cd.members m2 ON m2.memid = m1.recommendedby
ORDER BY
    memsname,
    memfname;

-- Q15
SELECT DISTINCT
    m2.firstname,
    m2.surname
FROM
    cd.members m1
        JOIN cd.members m2
             ON m2.memid = m1.recommendedby
ORDER BY
    m2.surname,
    m2.firstname;

-- Q16
SELECT DISTINCT
    m1.firstname || ' ' || m1.surname AS member,
    (
        SELECT
            m2.firstname || ' ' || m2.surname AS recommender
        FROM cd.members m2
        WHERE m2.memid = m1.recommendedby
    )
FROM cd.members m1
ORDER BY member;

-- Q17
SELECT
    recommendedby,
    COUNT(*) AS count
FROM cd.members
WHERE recommendedby IS NOT NULL
GROUP BY recommendedby
ORDER BY  recommendedby;

-- Q18
SELECT
    facid,
    SUM(slots) AS Total_Slots
FROM cd.bookings
GROUP BY facid
ORDER BY facid;

-- Q19
SELECT
    facid,
    SUM(slots) AS Total_Slots
FROM cd.bookings
WHERE starttime >= '2012-09-01'
  AND starttime < '2012-10-01'
GROUP BY facid
ORDER BY Total_Slots;

-- Q20
SELECT
    facid,
    EXTRACT(MONTH FROM starttime) AS month,
    SUM(slots) AS Total_Slots
FROM cd.bookings
WHERE EXTRACT(YEAR FROM starttime) = 2012
GROUP BY facid, EXTRACT(MONTH FROM starttime)
ORDER BY facid, month;

-- Q21
SELECT
    COUNT(DISTINCT memid) as count
FROM cd.bookings;

-- Q22
SELECT
    m.surname, m.firstname, m.memid,
    MIN(b.starttime) AS starttime
FROM cd.members m
         JOIN cd.bookings b ON m.memid = b.memid
WHERE b.starttime >= '2012-09-01'
GROUP BY m.surname, m.firstname, m.memid
ORDER BY m.memid;

-- Q23
SELECT
    COUNT(*)OVER() AS count,
    firstname, surname
FROM cd.members
ORDER BY joindate;

-- Q24
SELECT
    ROW_NUMBER()OVER(ORDER BY joindate) AS row_number,
    firstname, surname
FROM cd.members;

-- Q25
SELECT
    facid, total
FROM
    (
        SELECT
            facid,
            SUM(slots) AS total,
            RANK()OVER(ORDER BY SUM(slots) DESC) AS rnk
        FROM cd.bookings
        GROUP BY facid
    ) rank_by_total_slots
WHERE rnk = 1;

-- Q26
SELECT
    surname || ',' || firstname AS name
FROM cd.members;

-- Q27
SELECT
    memid, telephone
FROM cd.members
WHERE telephone ~ '[()]';

-- Q28
SELECT
    LEFT(surname, 1) AS letter,
    COUNT(*) AS count
FROM
    cd.members
GROUP BY LEFT(surname, 1)
ORDER BY letter;

```