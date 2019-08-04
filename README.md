# Log Analysis: Udacity Project

This project is for educational purpose to learn more about queries in SQL.
Given a relational database on PostgreSQL, I had to answer 3 question using
queries:

1) What are the three most popular articles of all time?
2) Who are the authors of most popular articles of all time?
3) On what days more than 1% of requests resulted in errors?

To do this I built a python program to connect to the database using `psycopg2`,
made some queries in SQL and display the results.

## Prerequisites

This project requires the following software to run:
[Python 2.7](https://www.python.org)
[VirtualBox](https://www.virtualbox.org)
[Vagrant](https://www.vagrantup.com)

Then use the vagrant file provided to build up the environment using the following command:
```
vagrant up
```
And to connect to the virtual server:
```
vagrant ssh
```

## Getting Started

The database can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
You can fetch data to PostgreSQL using the following command:

```
psql -d news -f newsdata.sql
```


### Creating Views

Views are automatically created by the `log_report.py` script. This steps are deprecated


In order to run some queries I had to create two views in PostgreSQL. This was made
to simplify the complexity of the question number 3. To create them you need to
access the virtual machine using the vagrant ssh command, and then access the psql news
database. Then type the following code on terminal:

View to show all errors by date
```sql
CREATE VIEW errorcount AS
SELECT time::date as date, count(time) as totalerrors
FROM log
WHERE status like '%404%'
GROUP BY date;
```

View to show all access dates
```sql
CREATE VIEW logcount AS
SELECT time::date as date, count(time) as totalcount
FROM log
GROUP BY date;
```

## Running the Log Analysis

To run connect to the virtual server and type `python log_report.py`
Don't forget to check if the file is in the virtual server and the database is
loaded and the views are created.
