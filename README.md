# Udacity
For Udacity Nanodegree projects

# Fullstack Developer Nanodegree Project 1: Logs Analysis

The project is intended to connect to and query the database of a newspaper site, and answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started (for Windows)

1. Download Vagrant [here](https://www.vagrantup.com/downloads.html).
2. Download VirtualBox [here](https://www.virtualbox.org/wiki/Downloads).
3. In a new directory, download and extract the FSND-Virtual-Machine included with the Fullstack Developer nanodegree [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
4. Navigate into the `FSND-Virtual-Machine` directory, and then into the `Vagrant` directory.
5. In the `Vagrant` directory, enter `Vagrant up`, and wait for up to an hour as Vagrant sets up. Resolve any version or port errors by making changes in `VagrantFile`, within the `Vagrant` directory (e.g. `nano VagrantFile`).
6. Once Vagrant is set up, enter `Vagrant SSH` to enter the virtual machine.
7. Download  `newsdata.sql` [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), and extract into the `FSND-Virtual-Machine\Vagrant` directory.
8. In the Vagrant directory, run `psql -d news -f newsdata.sql`.
9. For this project, run the project code (`python JoshC_Project1.py`) in the `FSND-Virtual-Machine\Vagrant` directory. Follow the menu prompts to receive answers to the selected questions.

## Structure of the Database

The following tables are included in the `news` database:

| Schema | Name     | Type  |
|--------|----------|-------|
| public | articles | table |
| public | authors  | table |
| public | log      | table |

Below are the columns and datatypes of the `articles` table in the `news` database:

| Column | Type                     | Modifiers                                             |
|--------|--------------------------|-------------------------------------------------------|
| author | integer                  | not null                                              |
| title  | text                     | not null                                              |
| slug   | text                     | not null                                              |
| lead   | text                     |                                                       |
| body   | text                     |                                                       |
| time   | timestamp with time zone | default now()                                         |
| id     | integer                  | not null default nextval('articles_id_seq'::regclass) |

Below are the columns and datatypes of the `authors` table in the `news` database:



| Column | Type    | Modifiers                                            |
|--------|---------|------------------------------------------------------|
| name   | text    | not null                                             |
| bio    | text    |                                                      |
| id     | integer | not null default nextval('authors_id_seq'::regclass) |

Below are the columns and datatypes of the `log` table in the `news` database:

| Column | Type                     | Modifiers                                        |
|--------|--------------------------|--------------------------------------------------|
| path   | text                     |                                                  |
| ip     | inet                     |                                                  |
| method | text                     |                                                  |
| status | text                     |                                                  |
| time   | timestamp with time zone | default now()                                    |
| id     | integer                  | not null default nextval('log_id_seq'::regclass) |

## SQL Queries Used (and Views)

See below for queries used (including views created) for each question:

**Question 1. What are the most popular three articles of all time**

Query1:

```
CREATE OR REPLACE VIEW articles_top AS
        SELECT TITLE,COUNT(title)
        AS VIEWS FROM articles,log
        WHERE log.path = concat('/article/',articles.slug)
        GROUP BY title
        ORDER BY VIEWS DESC
```

Query2:

```
SELECT * FROM articles_top LIMIT 3
```

**Question 2. Who are the most popular article authors of all time?**

Query1:

```
CREATE OR REPLACE VIEW authors_top AS
        SELECT authors.name,
        COUNT(articles.author) AS VIEWS FROM authors,
        log, articles
        WHERE articles.author = authors.id
        AND log.path = concat('/article/',articles.slug)
        GROUP BY authors.name
        ORDER BY VIEWS DESC
```

Query2:

```
SELECT * FROM authors_top LIMIT 3
```

**Question 3. On which days did more than 1% of requests lead to errors?**

Query:

```
SELECT to_char(date, 'DD FMMonth YYYY'),
    ((error_logs/all_logs)*100)
    FROM
        (select cast(time AS date) AS date,
        COUNT(*) AS all_logs,
        CAST(SUM(CAST((status <> '200 OK') AS int)) AS float)
    AS error_logs
    FROM log GROUP BY date)
AS error_rate
WHERE (error_logs/all_logs)*100 > 1;""")
```

## Sample Output

Running all question options produces the following answer output:

```
Printing all answer output...



Question 1: What are the three most popular articles in the database?

Querying 'news' database...

The top three articles in the 'news' database are:

Article: Candidate is jerk, alleges rival  Views: 338647
Article: Bears love berries, alleges bear  Views: 253801
Article: Bad things gone, say good people  Views: 170098



Question 2: Who are the most popular authors in the database?

Querying 'news' database...

The top three authors in the 'news' database are:

Author: Ursula La Multa  Views: 507594
Author: Rudolf von Treppenwitz  Views: 423457
Author: Anonymous Contributor  Views: 170098



Question 3: On which date(s) did more than 1% of requests lead to errors?

Querying 'news' database...

The following date(s) in the 'news' database had error rates of 1.0% or greater:

Date: 17 July 2016  Error Rate: 2.26%


Exiting...
```
