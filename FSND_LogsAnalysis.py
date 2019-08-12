#!/usr/bin/env python

import psycopg2
from time import sleep
import datetime

# The 'menu' section is only intended to add a fun interface to the project -
# nothing special, but it definitely made it quicker to run through any given
# answer without altering what functions are called in the code.

DBNAME = "news"


def intro():
    print("\n##############################################\n")
    print("Udacity, Full Stack Development Course")
    print("Project 1: Logs Analysis")
    print("Author: Josh Cavric")
    print("\n##############################################")
    sleep(1.0)


def top_articles():
    print("\nQuestion 1: What are the three most popular articles " +
          "in the database?\n")
    sleep(0.2)
    print("Querying '" + DBNAME + "' database...\n")
    db = psycopg2.connect(database=DBNAME)  # Connect to 'news' database
    c = db.cursor()
    query1 = ("""CREATE OR REPLACE VIEW articles_top AS
        SELECT TITLE,COUNT(title)
        AS VIEWS FROM articles,log
        WHERE log.path = concat('/article/',articles.slug)
        GROUP BY title
        ORDER BY VIEWS DESC""")
    query2 = ("""SELECT * FROM articles_top LIMIT 3""")
    c.execute(query1)
    c.execute(query2)
    results = c.fetchall()
    db.close()
    print("The top three articles in the '" + DBNAME + "' database are:\n")
    sleep(0.7)
    for i in range(len(results)):
        print("Article: " + results[i][0] + "  Views: " + str(results[i][1]))
        sleep(0.5)


def top_authors():
    print("\nQuestion 2: Who are the most popular authors in the database?\n")
    sleep(0.2)
    print("Querying '" + DBNAME + "' database...\n")
    db = psycopg2.connect(database=DBNAME)  # Connect to 'news' database
    c = db.cursor()
    query1 = ("""CREATE OR REPLACE VIEW authors_top AS
        SELECT authors.name,
        COUNT(articles.author) AS VIEWS FROM authors,
        log, articles
        WHERE articles.author = authors.id
        AND log.path = concat('/article/',articles.slug)
        GROUP BY authors.name
        ORDER BY VIEWS DESC""")
    query2 = ("""SELECT * FROM authors_top LIMIT 3""")
    c.execute(query1)
    c.execute(query2)
    results = c.fetchall()
    db.close()
    print("The top three authors in the '" + DBNAME + "' database are:\n")
    sleep(0.7)
    for i in range(len(results)):
        print("Author: " + results[i][0] + "  Views: " + str(results[i][1]))
        sleep(0.5)


def worst_error_days():
    print("\nQuestion 3: On which date(s) did more than " +
          "1% of requests lead to errors?\n")
    sleep(0.2)
    print("Querying '" + DBNAME + "' database...\n")
    db = psycopg2.connect(database=DBNAME)  # Connect to 'news' database
    c = db.cursor()
    query = ("""SELECT to_char(date, 'DD FMMonth YYYY'),
                ((error_logs/all_logs)*100)
                FROM
                    (select cast(time AS date) AS date,
                    COUNT(*) AS all_logs,
                    CAST(SUM(CAST((status <> '200 OK') AS int)) AS float)
                AS error_logs
                FROM log GROUP BY date)
                AS error_rate
                WHERE (error_logs/all_logs)*100 > 1;""")
    c.execute(query)
    results = c.fetchall()
    db.close()
    print("The following date(s) in the '" + DBNAME + "' database " +
          "had error rates of 1.0% or greater:\n")
    for i in range(len(results)):
        print("Date: " + str(results[i][0]) + "  Error Rate: "
              + (str(results[i][1]))[0:4]+"%\n")
        sleep(0.5)


def menu():

    choice = '0'

    print("\n\nPlease select an option:")
    sleep(0.4)
    print("\nSelect 1 for the Top 3 Articles in the database (Question 1).")
    print("\nSelect 2 for the Top 3 Authors in the database (Question 2).")
    print("\nSelect 3 for the Worst Error Days in the Database (Question 3).")
    print("\nSelect 4 to print all answer output.")
    print("\nSelect 5 to exit.\n")

    while choice == '0':
        choice = input("Please select an option: ")

    if choice == 1:
        print("\n\nOption 1 selected.")
        sleep(0.8)
        top_articles()
        print("\nReturning to main menu.")
        sleep(1.0)
        menu()
    elif choice == 2:
        print("\n\nOption 2 selected.")
        sleep(0.8)
        top_authors()
        print("\nReturning to main menu.")
        sleep(1.0)
        menu()
    elif choice == 3:
        print("\n\nOption 3 selected.")
        sleep(0.8)
        worst_error_days()
        print("Returning to main menu.")
        sleep(1.0)
        menu()
    elif choice == 4:
        print("\n\nOption 4 selected. Printing all answer output...")
        sleep(0.8)
        print("\n")
        top_articles()
        print("\n")
        top_authors()
        print("\n")
        worst_error_days()
        print("\nExiting...\n\n")
        exit()
    elif choice == 5:
        print("\n\nOption 5 selected.")
        sleep(0.5)
        print("\nExiting.\n\n")
        sleep(0.2)
        exit()
    else:
        print("\n\nSelection unavailable. Please select a valid option.")
        sleep(1.0)
        menu()


intro()


menu()
