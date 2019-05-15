# udacityClass
### Project1 : News Website Logs Analysis Statistics
This project sets up a **PostgreSQL** database for a **news** website.
The provided Python script **project1.py** uses the **psycopg2** library to query the database and produce a report that answers the following questions:
1. What are the most popular three articles of all time?
#Answer:
- "Candidate is jerk, alleges rival" -- 338647 views
- "Bears love berries, alleges bear" -- 253801 views
- "Bad things gone, say good people" -- 170098 views
2. Who are the most popular article authors of all time?
#Answer:
- Ursula La Multa -- 507594 views
- Rudolf von Treppenwitz -- 423457 views
- Anonymous Contributor -- 170098 views
- Markoff Chaney -- 84557 views
3. On which days did more than 1% of requests lead to errors?
#Answer:
- Jul 17,2016 -- 2.26% errors
#### Requirements
- Python
- PostgreSQL
- psycopg2 library
- Please download news database: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
- Import news database: e.g. $ psql -d news -f news_sql_database_file.sql
### Usage
1. run the command first: create view log_view as select path,count(*) as num from log group by path having path!='/' order by num desc;
2. run the command: python project1.py
