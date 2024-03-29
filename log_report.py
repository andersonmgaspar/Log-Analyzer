#!/usr/bin/env python

import psycopg2

DBNAME = "news"

top3_articles = """select title, count(log.id) as views
                   from articles, log
                   where articles.slug = substring(log.path,10)
                   group by articles.title
                   order by views DESC LIMIT 3;"""

popular_authors = """select authors.name, count(log.id) as views
                     from articles, authors, log
                     where articles.slug = substring(log.path, 10)
                     and authors.id = articles.author
                     group by authors.name
                     order by views DESC;"""

error_count = """SELECT errorcount.date, round(100.0*totalerrors/totalcount,2)
                 as percent
                 FROM errorcount, logcount
                 WHERE logcount.date = errorcount.date
                 AND totalerrors > totalcount/100; """


# Generic function to get a result from a query;
def make_query(query):
    try:
        connection = psycopg2.connect(database=DBNAME)
        cursor = connection.cursor()
        cursor.execute(query)
        posts = cursor.fetchall()
        return posts
    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()


def create_views(file):
    try:
        connection = psycopg2.connect(database=DBNAME)
        cursor = connection.cursor()
        views = open(file).read()
        cursor.execute(views)
        return true
    except (Exception, psycopg2.Error) as error:
        print ("Error while creating views from PostgreSQL", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()


def show_results(query_statement, query):
    results = make_query(query)
    print("")
    print(query_statement)
    for row in results:
        author = str(row[0])
        result_views = str(row[1])
        print(author + " with " + result_views + " views.")
    print("")

if __name__ == '__main__':
    create_views('create.views.sql')
    show_results("What are the most popular three articles of all time? ",
                 top3_articles)
    show_results("Who are the most popular article authors of all time? ",
                 popular_authors)
    errors = make_query(error_count)
    print("On which days more than 1% of the requests led to error?")
    print(str(errors[0][0]) + " - " + str(errors[0][1]) + "%")
