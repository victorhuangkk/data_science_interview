grade## This doc contains SQL summary and problem sets copied from various websites:
1. SQL ZOO [links](https://sqlzoo.net/)
2. Mode Analytics [links](https://mode.com/sql-tutorial/)
3. SQL 50 Problems [links](https://blog.csdn.net/flycat296/article/details/63681089)
4. Hacker Rank [links](https://www.hackerrank.com/domains/sql)
5. LeetCode [links](https://leetcode.com/problemset/database/)
6. CMU Intro to Database 2018 [links](https://https://15445.courses.cs.cmu.edu/fall2018/)


----
## How to use this file?
Feel free to comment on it or use it as your study/review material for SQL.
And it is highly recommended to download a MySQL workbench to your local computer. You may not learn effectively without hands-on experience.


## Who is the target audience?
This summary is for data analyst/business analyst/market analyst. So, if you are computer science expert, you may feel it is a bit too easy.

## Personal Summary

SQL is similar to plain English. So, we should obey its internal grammar. Although you may not be a native speaker, SQL should make sense to you if we do some anatommy. So, please follow me and take a breathtaking journey.

# Remarks
Before we get started, I should mention that SQL is different from the most programming language.
1. SQL is not sensitive to blank.
2. SQL is not sensitive to capital letters.
However, it is suggested to keep a good SQL writing style. For me, I would paste my SQL queries to Mode Analytics and let it help me format them.  

## Select

```sql
SELECT *
  FROM tbl1
```
This is the simplest query will show you all the content in table named tbl1. There are two key points:
1. This query may be time consuming, so you may add ```sql  limit 10``` to contain the number of rows.
2. This query is useful when you want to know all the columns in that table, function similar to ```R list(df)``` in R or Python.

# Basics
SQL language is similar to plain English. So, it is composed by three main components.

``` sql
select * from tbl1 where
```
1. select is to choose which feature you want to display
2. from is the source
3. where is condition

Except select, all other components are not required by the system. However, in most cases, our query should be composed by these three parts.

# Alias
When selecting a column or a table, you can give it another name. I will specify it later. In general, it has two purposes:
1. Shorten the spelling. For example, we can specify student as s1.
2. Enable SQL to distinguish the table. And it has two sub cases. First, when we need self join, SQL cannot distinguish which table we specify without alias. Secondly, when the subquery returns a temperoary table, MySQL require the user to give that table a name.

For illustration purposes. Here is the code




## Thanks
I would appreciate any comment and suggestion.
