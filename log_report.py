import psycopg2

DBNAME = "news"

top3_articles = """select title, count(log.id) as views
                   from articles, log
                   where articles.slug = substring(log.path,10)
                   group by articles.title
                   order by views DESC LIMIT 3;"""

popular_authors =  """select authors.name, count(log.id) as views
                      from articles, authors, log
                      where articles.slug = substring(log.path, 10)
                      and authors.id = articles.author
                      group by authors.name
                      order by views DESC;"""

# View to show all errors by date
"""
CREATE VIEW errorcount AS
SELECT time::date as date, count(time) as totalerrors
FROM log
WHERE status like '%404%'
GROUP BY date;
"""

# View to show all access dates
"""
CREATE VIEW logcount AS
SELECT time::date as date, count(time) as totalcount
FROM log
GROUP BY date;
"""

error_count = """SELECT errorcount.date, round(100.0*totalerrors/totalcount,2) as percent
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
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# Show Popular Authors
def show_results(query_statement, query):
        results = make_query(query)
        print("");
        print(query_statement)
        for row in results:
           author = str(row[0])
           result_views = str(row[1])
           print(author + " - " + result_views)
        print("");


show_results("Top 3 Articles: ", top3_articles)
show_results("Popular Authors: ", popular_authors)
show_results("Dates with access problems: ", error_count)