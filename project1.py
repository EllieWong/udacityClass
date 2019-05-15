#!/usr/bin/env python
# Projct1 homework

import psycopg2

DBNAME = 'news'


def getTop3Articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
SELECT title,
       num
FROM articles
JOIN log_view ON log_view.path=concat('/article/', articles.slug)
ORDER BY num DESC
LIMIT 3;
""")
    results = c.fetchall()
    db.close()
    for result in results:
        # print ("\"%s\" -- %s views"%result)
        print '"{article}" -- {count} views'.format(article=result[0], count=result[1])


def getTopAuthors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
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
""")
    results = c.fetchall()
    db.close()
    for result in results:
        print ("%s -- %s views" % result)


def getFailurate():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
SELECT *
FROM
  (SELECT total.date,
          round((cast(error.pv AS numeric) / total.pv * 100), 2) AS failure
   FROM
     (SELECT to_char(TIME, 'Mon DD,YYYY') AS date,
             count(*) AS pv
      FROM log
      WHERE status!='200 OK'
      GROUP BY date) AS error
   JOIN
     (SELECT to_char(TIME, 'Mon DD,YYYY') AS date,
             count(*) AS pv
      FROM log
      GROUP BY date) AS total ON error.date=total.date) AS FINAL
WHERE failure>1;
""")
    results = c.fetchall()
    db.close()
    for result in results:
        print ("%s -- %0.2f%% errors" % result)


if __name__ == '__main__':
    print 'question1: What are the most popular three articles of all time? '
    getTop3Articles()
    print
    print 'question2: Who are the most popular article authors of all time?'
    getTopAuthors()
    print
    print 'question3: On which days did more than 1% of requests lead to errors? '
    getFailurate()
