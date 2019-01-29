<link rel="stylesheet" type="text/css" href="auto-number-title.css" />
# SQL 50 Problems.
## Please follow the commands here to create your own tables for the these Problems

Create student table
``` sql
create table student(SId varchar(10),Sname varchar(10),Sage datetime,Sgender varchar(10));
insert into Student values('01' , 'zhaolei' , '1990-01-01' , 'male');
insert into Student values('02' , 'qiandian' , '1990-12-21' , 'male');
insert into Student values('03' , 'sunfeng' , '1990-05-20' , 'male');
insert into Student values('04' , 'liyun' , '1990-08-06' , 'male');
insert into Student values('05' , 'zhoumei' , '1991-12-01' , 'female');
insert into Student values('06' , 'wulan' , '1992-03-01' , 'female');
insert into Student values('07' , 'zhengzhu' , '1989-07-01' , 'female');
insert into Student values('09' , 'zhangsan' , '2017-12-20' , 'female');
insert into Student values('10' , 'lisi' , '2017-12-25' , 'female');
insert into Student values('11' , 'lisi' , '2017-12-30' , 'female');
insert into Student values('12' , 'zhaoliu' , '2017-01-01' , 'female');
insert into Student values('13' , 'sunqi' , '2018-01-01' , 'female');
```
Create course table
``` sql
create table course(CId varchar(10),Cname nvarchar(10),TId varchar(10))
insert into Course values('01' , 'yuwen' , '02')
insert into Course values('02' , 'shuxue' , '01')
insert into Course values('03' , 'yingyu' , '03')
```

Create teacher table
```sql
create table teacher(TId varchar(10),Tname varchar(10))
insert into Teacher values('01' , 'zhangsan')
insert into Teacher values('02' , 'lisi')
insert into Teacher values('03' , 'wangwu')
```

Create grade table
```sql
create table grade(SId varchar(10),CId varchar(10),score decimal(18,1))
insert into grade values('01' , '01' , 80)
insert into grade values('01' , '02' , 90)
insert into grade values('01' , '03' , 99)
insert into grade values('02' , '01' , 70)
insert into grade values('02' , '02' , 60)
insert into grade values('02' , '03' , 80)
insert into grade values('03' , '01' , 80)
insert into grade values('03' , '02' , 80)
insert into grade values('03' , '03' , 80)
insert into grade values('04' , '01' , 50)
insert into grade values('04' , '02' , 30)
insert into grade values('04' , '03' , 20)
insert into grade values('05' , '01' , 76)
insert into grade values('05' , '02' , 87)
insert into grade values('06' , '01' , 31)
insert into grade values('06' , '03' , 34)
insert into grade values('07' , '02' , 89)
insert into grade values('07' , '03' , 98)
```

## Join Table

###  Find when a student register both course '01' and course '02'.

Logic: To find common entries in two tables, we should naturally use inner join.

```sql
SELECT g1.GId, g1.CId, g1.score, g2.CId, g2.score
FROM
    (SELECT *
   FROM grade
   WHERE CId = '01') AS g1
JOIN
  (SELECT *
   FROM grade
   WHERE CId = '02') AS g2
  ON g1.GId = g2.GId;

```

###  Find entries whose course '01' has higher score than course '02'

Logic: Obviously, this is a self-join problem. On column in the table shows course number and another shows the score. So, we can solve it by creating one table containing score for class 1 and another table contain score for class 2. Then, join these two tables by students' ID. After that, student's info can be found in student table. We just do a simple inner join to find out students' info as requsted.

```sql
SELECT *
FROM
    (SELECT g1.GId,
            g1.score
   FROM grade g1
   JOIN grade g2
     ON (g1.GId = g2.GId)
     WHERE g1.CId = '01'
       AND g2.CId = '02'
       AND g1.score > g2.score) AS tbl1
JOIN student s1
  ON tbl1.GId = s1.SId;
```

#### Remarks
The previous two queries funcion similarly. However, we always want to filter as early as possible. In marketing, this is calles marketing funnel.

### Find entries when course '01' exist but course '02' may not exist.

Logic: This is when we should use left(right) join.

```sql
SELECT *
FROM
    (SELECT *
   FROM grade
   WHERE CId = '01') AS g1
left join
  (SELECT *
   FROM grade
   WHERE CId = '02') AS g2
  ON g1.GId = g2.GId;
```

### Find entries when course '01' do not exist but course '02' exist.

Logic: This case is to find out difference set. However, MySQL dosen't support direct differencing calculation. So, we can use left(right) join to find out null values. Then, use where to constrain that.

```sql
SELECT GId,
       cid2 from
  (SELECT g2.GId, g1.CId AS cid1, g2.CId AS cid2
   FROM
       (SELECT *
      FROM grade
      WHERE CId = '01') AS g1
   right join
     (SELECT *
      FROM grade
      WHERE CId = '02') AS g2
     ON g1.GId = g2.GId) AS tbl1
WHERE tbl1.cid1 is null;
```

At the same time, we can use another version, subquery to simplify our calculation. However, it is more expensive.

```sql
SELECT *
FROM grade
WHERE CId = '02'
  AND GId not in
    (SELECT GId
     FROM grade
     WHERE CId = '01');
```

### Find records with students who have score in grade table.

Logic: Very similar to previous question. Just use similar

```sql
SELECT distinct GId,
                SName,
                Sage
FROM grade
JOIN student
  ON grade.GId = student.SId;

```

### Find all students' info with their registration info, regardless how many classes they registered.

```sql
SELECT *
FROM student s1
JOIN grade g1
  ON s1.SId = g1.GId
JOIN course c1
  ON g1.CId = c1.CId;
```

### Find students's name, course ID and score for whom have at least one class is above 70.

```sql
SELECT g1.GId,
       s1.SName,
       g1.score,
       c1.Cname
FROM grade g1
JOIN student s1
  ON (g1.GId = s1.SId)
JOIN course c1
  ON (g1.CId = c1.CId)
  WHERE score > 70;
```

### Select failed courses
```sql
SELECT s1.Sname,
       c1.Cname,
       g1.score
FROM grade g1
JOIN student s1
  ON g1.GId = s1.SId
JOIN course c1
  ON g1.CId = c1.CId
  WHERE score <= 60;
```

### Find students' name and ID of their course number '01' and with score higher than 80.

```sql
SELECT s1.SId,
       s1.SName
FROM grade g1
JOIN student s1
  ON (g1.GId = s1.SId)
  WHERE score >= 80
    AND CId= '01';
```

### Find students' name and ID who took shuxue class and score is less than 60.

```sql
SELECT Sname,
       score
FROM student s1
JOIN grade g1 ON (s1.SId = g1.GId)
WHERE CId =
    (SELECT CId
     FROM course
     WHERE Cname = 'shuxue')
  AND score < 60;
```

### Find students' name who didn't register any class taught my 'zhangsan'.

Logic: This is a computational better way, compared with subqueries.

```sql
SELECT s1.SName
FROM student s1
JOIN grade g1
  ON s1.SId = g1.GId
JOIN course c1
  ON g1.CId = c1.CId
JOIN teacher t1
  ON c1.TId = t1.TId
  WHERE t1.Tname = 'zhangsan';
```

Logic: subquery accomplish the same task. It may be more intuitive when first
approach the problem, but is computationally expensive.

```sql
SELECT SName
FROM student
WHERE SId not in
    (SELECT GId
     FROM grade
     WHERE CId in
         (SELECT CId
          FROM course
          WHERE TId in
              (SELECT TId
               FROM teacher
               WHERE Tname = 'zhangsan')) );
```

### Find the number of students in each class.

```sql
SELECT CId,
       count(GId)
FROM grade
GROUP BY CId;
```

### Find students who register exactly two classes.

```sql
SELECT SId,
       Sname
FROM student
WHERE SId in
    (SELECT GId
     FROM grade
     GROUP BY GId
     HAVING count(CId) = 2);
```

### Find the number of male and female students.

```sql
SELECT Sgender,
       count(*)
FROM student
GROUP BY Sgender;
```

### Find a list of people who have the same and count the number.

Logic: It is an example of implicit self join.

```sql
SELECT *
FROM student s1,
     student s2
WHERE s1.SId != s2.SId
  AND s1.SName = s2.SName;
```

## Simple Select

### Find students' info who have records in grade table.

Logic: Use subquery to select student's ID number in grade table. Add this condition as contraints in where predicates of the main query.

```sql
SELECT *
FROM student
WHERE SId in
    (SELECT distinct GId
     FROM grade);
```

### Find the number of teacher who's last name is 'li'.

```sql
SELECT count(TId)
FROM teacher
WHERE Tname like 'li%';
```

### Find students' info whose name has feng
```sql
SELECT *
FROM student
WHERE SName like '%feng%';
```

### Find students' info for who have taken instructor 'zhangsan''s class.

Logic: instructor 'zhangsan' is the key to filter. There are two ways. We may use several subqueries to do the filter. However, it may not be computationally effective. So, the query may be rewritten by joins.

```sql
SELECT *
FROM student
WHERE SId in
    (SELECT GId
     FROM grade
     WHERE CId =
         (SELECT CId
          FROM course
          WHERE TId =
              (SELECT TId
               FROM teacher
               WHERE Tname = 'zhangsan') ));
```

## Aggregate Functions

### Find records with average socre is at least 60 with students' info and average score.

```sql
SELECT SId,
       Sname,
       AveScore
FROM
  (SELECT GId,
          avg(score) AS AveScore
   FROM grade
   GROUP BY GId
   HAVING AveScore >= 60) AS tbl1
JOIN student
  ON tbl1.GId = student.SId
ORDER BY AveScore DESC;
```

### Find all students' ID, name, number of registered courses and total score for all courses (no score use null)

Logic: We used two tables in this example. Use student table to fetch all students' information and use grade table to select score that they get from every course.

```sql
SELECT s1.*,
       total_courses,
       total_scores
FROM
    (SELECT GId,
            count(score) AS total_courses,
            sum(score) AS total_scores
   FROM grade
   GROUP BY GId) AS tbl1
right join student AS s1
  ON (tbl1.GId = s1.SId);
```


### Find students' info for whom do not register all courses.

Logic: Add criteria in having (similar to where) to filter a subquery.

```sql
SELECT *
FROM student
WHERE SId not in
    (SELECT GId
     FROM grade
     GROUP BY GId
     HAVING count(*) =
       (SELECT count(CId)
        FROM course));
```


### Find students' info who register at least one same class with student '01'.

Logic: The trick here good. Create a criteria to include all the classes that student '01'
regitered. Then, sum them up to compare with other students.

```sql
SELECT s1.*
FROM grade g1
JOIN student s1
  ON (g1.GId = s1.SId)
WHERE g1.CId in
    (SELECT CId
     FROM grade
     WHERE GId = '01')
  AND g1.GId != '01'
GROUP BY g1.GId
HAVING sum(g1.CId) >= 0);
```

### Find students' info who register exactly the same class with student '01'

```sql
SELECT s1.*
FROM grade g1
JOIN student s1
  ON (g1.GId = s1.SId)
WHERE g1.CId in
    (SELECT CId
     FROM grade
     WHERE GId = '01')
  AND g1.GId != '01'
GROUP BY g1.GId
HAVING sum(g1.CId) >=
  (SELECT sum(CId)
   FROM grade
   WHERE GId = '01');
```

### Search students' info for whom register all classes.

```sql
SELECT *
FROM student
WHERE SId in
    (SELECT GId
     FROM grade
     GROUP BY GId
     HAVING count(GId) =
       (SELECT count(*)
        FROM course));
```

### Search students' ID for who register more than 2 classes.

```sql
SELECT SId,
       Sname
FROM student join
    (SELECT GId, count(GId) AS num_courses
   FROM grade
   GROUP BY GId
   HAVING num_courses >= 2) tbl
  ON (student.SId = tbl.GId);
```

### Rank students' by their classes' score and average score

```sql
SELECT *
FROM
    (SELECT GId,
            avg(score) AS average
   FROM grade
   GROUP BY GId
   ORDER BY average DESC) AS tbl1
right join grade
  ON (tbl1.GId = grade.GId)
```

### Find each class's average score, order by average in desceding order and order by class ID in ascending order.

```sql
SELECT grade.CId,
       avg(score) AS grade_ave,
       course.Cname
FROM grade
JOIN course
  ON grade.CId = course.CId
GROUP BY CId
ORDER BY grade_ave DESC,
         CId;
```

### Find students' ID, name and average score higher or equal to 85.

```sql
SELECT grade.GId,
       student.Sname,
       round(avg(score),2) AS grade_ave
FROM grade
JOIN student
  ON grade.GId = student.SId
GROUP BY GId
HAVING grade_ave >= 80
ORDER BY grade_ave DESC;
```

### 检索" 01 "课程分数小于 60，按分数降序排列的学生信息

select * from
(select GId, avg(score) as average
from grade
group by GId
order by average DESC) as tbl1 right join grade on (tbl1.GId = grade.GId)


### 求每门课程的学生人数

select CId,
count(CId) as 'students_num'
from grade
group by CId;

## Window Function

Basic: func() over (partition by A order by B)
A is the second order column, B is the first order column or raw data column.

### Rank by each course's score and show rank, Score ties are assigned the same rank, with the next ranking(s) skipped

 ```sql
 SELECT GId,
        score,
        rank() over (partition BY CId
                     ORDER BY score DESC)
 FROM grade;
```

### Rank by each course's score and show rank, Score ties are assigned the same rank, with the consecutive ranking(s)

```sql
SELECT GId,
       score,
       dense_rank() over (partition BY CId
                          ORDER BY score DESC)
FROM grade;
```

### Find first two highest scores for each course.

Logic: The highest two could be filtered by window function. Apply rank function to these columns.

```sql
SELECT *
FROM
  (SELECT GId,
          score,
          CId,
          row_number() over (partition BY CId
                             ORDER BY score DESC) AS rank_num
   FROM grade) AS tbl
JOIN student
  ON (tbl.GId = student.SId)
WHERE rank_num <= 2
ORDER BY CId;
```

### Find students' total score, rank them. If tie, leave blank/ If tie, do consecutive ranking.

Logic: ranking is done by rank() function in MySQL. Even though it could be done by custom variable, rank() is easier.

```sql
SELECT GId,
       sum(score),
       rank() OVER (
                    ORDER BY sum(score) DESC)
FROM grade
GROUP BY GId
ORDER BY sum(score) DESC;
```

Logic: The only difference is that consecutive ranking is done by dense_rank() function.

```sql
SELECT GId,
       sum(score),
       dense_rank() OVER (
                          ORDER BY sum(score) DESC)
FROM grade
GROUP BY GId
ORDER BY sum(score) DESC;
```

## SQL Logic Statement

### Find The Following Data：

Include: Class ID, Class Name, Highest Score, Lowest Score, Average Score, Pass rate, C rate, B rate, A rate,
numer of students registered. Order by register number in descending and class ID ascending.

1. A: >= 90
2. B: 80-90
3. C: 70-80
4. Pass >= 60

Logic: The self-defined parameters can be calculated by the combination of the following
1. sum()/count()
2. case when then else end
3. between is easy in most cases but remember between A and B: A < B

```sql
SELECT g1.CId AS courseID,
       c1.CName AS courseName,
       MAX(g1.score)AS max_score,
       MIN(g1.score)AS min_score,
       AVG(g1.score)AS ave_score,
       count(*)AS register_num,
       sum(CASE
               WHEN g1.score>=60 then 1
               ELSE 0
           END)/count(*)AS pass_rate,
       sum(CASE
               WHEN g1.score between 70 AND 80 then 1
               ELSE 0
           END)/count(*)AS 'C',
       sum(CASE
               WHEN g1.score between 80 AND 90 then 1
               ELSE 0
           END)/count(*)AS 'B',
       sum(CASE
               WHEN g1.score>=90 then 1
               ELSE 0
           END)/count(*)AS 'A'
FROM grade AS g1
JOIN course c1
  ON (g1.CId = c1.CId)
GROUP BY g1.CId
ORDER BY count(*) DESC, g1.CId
```

### Find students's ID, name and average score for who dosen't pass two or more classes.

Logic:

```sql
SELECT grade.GId,
       SName,
       avg(score) AS average
FROM grade
JOIN student
WHERE grade.GId = student.SId
GROUP BY grade.GId
HAVING sum(CASE
               WHEN score < 60 then 1
               ELSE 0
           END) >= 2
```


### 统计各科成绩各分数段人数：课程编号，课程名称，[100-85]，[85-70]，[70-60]，[60-0] 及所占百分比

Find

```sql
SELECT course.Cname,
       t1.*
FROM course
LEFT JOIN
    (SELECT grade.CId,
            CONCAT(round(sum(CASE
                                 WHEN grade.score between 85 AND 100 then 1
                                 ELSE 0
                             END)/count(*)*100,2),'%') AS '[85-100]',
            CONCAT(round(sum(CASE
                                 WHEN grade.score between 70 AND 85 then 1
                                 ELSE 0
                             END)/count(*)*100,2),'%') AS '[70-85)',
            CONCAT(round(sum(CASE
                                 WHEN grade.score between 60 AND 70 then 1
                                 ELSE 0
                             END)/count(*)*100,2),'%') AS '[60-70)',
            CONCAT(round(sum(CASE
                                 WHEN grade.score between 0 AND 60 then 1
                                 ELSE 0
                             END)/count(*)*100,2),'%') AS '[0-60)'
   FROM grade
   GROUP BY grade.CId) AS t1
  ON course.CId=t1.CId;
```

### Count the number of students in each class (greater than 5 students)

```sql
SELECT CId,
       (CASE
            WHEN count(CId) > 5 then count(CId)
            ELSE 'not enough students'
        END) AS 'students_num'
FROM grade
GROUP BY CId;
```

# SQL Time Functions

### Find a list of students who born at 1990.

```sql
SELECT SId,
       SName,
       YEAR(Sage) AS born_year
FROM student
HAVING born_year = '1990';
```

### Find students' age, only cares about year.

```sql
SELECT Sname,
       year(curdate()) - year(Sage) AS age
FROM student;
```

### Find students' exact age.

```sql
SELECT Sname,
       round(DATEDIFF(curdate(), SAge)/365,0) AS age
FROM student;
```

### Find students' birthday in this week.

```sql
SELECT *
FROM student
WHERE YEARWEEK(student.Sage)=YEARWEEK(CURDATE());
```

### Find students' birthday in next week.

```sql
SELECT *
FROM student
WHERE YEARWEEK(student.Sage)=YEARWEEK(CURDATE()) + 1;
```

### Find students' birthday in this month.

```sql
SELECT *
FROM student
WHERE month(student.Sage)=month(CURDATE());
```

### Find students' birthday in next month.

```sql
SELECT *
FROM student
WHERE month(student.Sage)=month(CURDATE()) + 1;
```


### 查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩

select distinct s1.Sname, g1.GId, g1.CId, g1.score
from grade g1
inner join grade g2 on g1.GId = g2.GId
inner join student s1 on g1.GId = s1.SId
where g1.CId != g2.CId
and g1.score = g2.score;

### 成绩不重复，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩

```sql
select student.*,grade.score
from student ,course ,teacher ,grade
where course.CId=grade.CId
and course.TId=teacher.TId
and teacher.Tname='zhangsan'
and student.SId =grade.GId
order by grade.GId
LIMIT 1
```
### 成绩有重复的情况下，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩

Should be very similar to the previous two
