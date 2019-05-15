#!/usr/bin/env python
# Projct1 homework

import psycopg2

DBNAME = 'news'


def executeQuery(sqlStatement):
    """
    return the query result
"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sqlStatement)
    results = c.fetchall()
    db.close()
    return results


def getTop3Articles():
    """
    get the most popular three articles of all time
"""
    statement = """
SELECT title,
       num
FROM articles
JOIN log_view ON log_view.path=concat('/article/', articles.slug)
ORDER BY num DESC
LIMIT 3;
"""
    results = executeQuery(statement)
    for result in results:
        print '"{art}" -- {num} views'.format(art=result[0], num=result[1])


def getTopAuthors():
    """
    get the most popular article authors of all time
"""
    statement = """
SELECT authors.name,
       article_log.pv
FROM
  (SELECT article1.author AS author,
          sum(log1.pv) AS pv
   FROM
     (SELECT author,
             slug,
             concat('/article/', slug) AS PATH
      FROM articles
      GROUP BY author,
               slug,
               concat('/article/', slug)) article1
   JOIN
     (SELECT PATH,
             count(1) AS pv
      FROM log
      GROUP BY PATH) log1 ON article1.path = log1.path
   GROUP BY article1.author) article_log
JOIN authors ON article_log.author = authors.id
ORDER BY article_log.pv DESC;
"""
    results = executeQuery(statement)
    for result in results:
        print '{author} -- {num} views'.format(author=result[0], num=result[1])


def getFailurate():
    """
    get those days, which more than 1% of requests lead to error
"""
    statement = """
SELECT *
FROM
  (SELECT to_char(total.date,'Mon DD,YYYY'),
          round((cast(error.pv AS numeric) / total.pv * 100), 2) AS failure
   FROM
     (SELECT time::date AS date,
             count(*) AS pv
      FROM log
      WHERE status!='200 OK'
      GROUP BY date) AS error
   JOIN
     (SELECT time::date AS date,
             count(*) AS pv
      FROM log
      GROUP BY date) AS total ON error.date=total.date) AS FINAL
WHERE failure>1;
"""
    results = executeQuery(statement)
    for result in results:
        print "{date} -- {rate}% errors".format(date=result[0], rate=result[1])


if __name__ == '__main__':
    print '1. What are the most popular three articles of all time? '
    getTop3Articles()
    print
    print '2. Who are the most popular article authors of all time? '
    getTopAuthors()
    print
    print '3. On which days did more than 1% of requests lead to errors?'
    getFailurate()
