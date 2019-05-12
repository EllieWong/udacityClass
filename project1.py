#Projct1 homework

import psycopg2

DBNAME='news'

def getTop3Articles():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select title, num from articles join log_view on log_view.path=concat('/article/',articles.slug) order by num desc limit 3;")
  results = c.fetchall()
  db.close()
  for result in results:
    print ("\"%s\" -- %s views"%result)
  

def getTopAuthors():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("""select authors.name, article_log.pv
from (
    select article1.author as author, sum(log1.pv) as pv
    from (
        select author, slug, concat('/article/', slug) as path 
        from articles 
        group by author, slug, concat('/article/', slug)
    ) article1
    join (
        select path, count(1) as pv 
        from log group by path
    ) log1
    on article1.path = log1.path
    group by article1.author
) article_log
join authors
on article_log.author = authors.id
order by article_log.pv desc;""")
  results = c.fetchall()
  db.close()
  for result in results:
    print("%s -- %s views"%result)

def getFailurate():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("""select * from (
select total.date, round((cast(error.pv as numeric) / total.pv * 100), 2) as failure
from (
    select to_char(time,'Mon DD,YYYY') as date,count(*) as pv from log where status!='200 OK' group by date
) as error 
join (
    select to_char(time,'Mon DD,YYYY') as date,count(*) as pv from log group by date 
) as total
on error.date=total.date
) as final where failure>1;""")
  results = c.fetchall()
  db.close()
  for result in results:
    print("%s -- %0.2f%% errors"%result)


if __name__ == '__main__':
  print 'question1: What are the most popular three articles of all time? '
  getTop3Articles()
  print
  print 'question2: Who are the most popular article authors of all time?'
  getTopAuthors()
  print 
  print 'question3: On which days did more than 1% of requests lead to errors? '
  getFailurate()
