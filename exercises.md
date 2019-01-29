## SQL 50 Problems.

# Please follow the commands here to create your own tables for the these Problems

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

# Join Table

## 1. Find when a student register both course '01' and course '02'.

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

## 2. Find entries whose course '01' has higher score than course '02'

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

### Remarks
The previous two queries funcion similarly. However, we always want to filter as early as possible. In marketing, this is calles marketing funnel.

## 3. Find entries when course '01' exist but course '02' may not exist.

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

## 4. Find entries when course '01' do not exist but course '02' exist.

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

## 5. Find records with students who have score in grade table.

Logic: Very similar to previous question. Just use similar

```sql
SELECT distinct GId,
                SName,
                Sage
FROM grade
JOIN student
  ON grade.GId = student.SId;

```

# Simple Select

## 1. Find students' info who have records in grade table.

Logic: Use subquery to select student's ID number in grade table. Add this condition as contraints in where predicates of the main query.

```sql
SELECT *
FROM student
WHERE SId in
    (SELECT distinct GId
     FROM grade);
```

## 2. Find the number of teacher who's last name is 'li'.

```sql
select count(TId)
from teacher
where Tname like 'li%'
```

## 3. Find students' info for who have taken instructor 'zhangsan''s class.

Logic: instructor 'zhangsan' is the key to filter. There are two ways. We may use several subqueries to do the filter. However, it may not be computationally effective. So, the query may be rewritten by joins.

```sql
select * from student where
SId in(
select GId from grade where CId =
(select CId from course where TId =
(select TId from teacher
where Tname = 'zhangsan')
));
```

# Aggregate Functions

## 1. Find records with average socre is at least 60 with students' info and average score.

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

## 2. Find all students' ID, name, number of registered courses and total score for all courses (no score use null)

Logic: We used two tables in this example. Use student table to fetch all students' information and use grade table to select score that they get from every course.

```sql
select s1.*, total_courses, total_scores from
(select GId, count(score) as total_courses, sum(score) as total_scores
from grade
group by GId) as tbl1 right join student as s1
on (tbl1.GId = s1.SId);
```


## 3. Find students' info for whom do not register all courses.

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


## 4. Find students' info who register at least one same class with student '01'.


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

## 5. Find students' info who register exactly the same class with student '01'

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


## 6. Find students' name who didn't register any class taught my 'zhangsan'.

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

##  Find the number of students in each class.

```sql
SELECT CId,
       count(GId)
FROM grade
GROUP BY CId;
```

## Find students who register exactly two classes.

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

## Find the number of male and female students.

```sql
SELECT Sgender,
       count(*)
FROM student
GROUP BY Sgender;
```

## Find a list of people who have the same and count the number.

Logic: It is an example of implicit self join.

```sql
SELECT *
FROM student s1,
     student s2
WHERE s1.SId != s2.SId
  AND s1.SName = s2.SName;
```

# Window Function

Basic: func() over (partition by A order by B)
A is the second order column, B is the first order column or raw data column.

## 1. Rank by each course's score and show rank, Score ties are assigned the same rank, with the next ranking(s) skipped

 ```sql
 SELECT GId,
        score,
        rank() over (partition BY CId
                     ORDER BY score DESC)
 FROM grade;
```

## 2. Rank by each course's score and show rank, Score ties are assigned the same rank, with the consecutive ranking(s)

```sql
SELECT GId,
       score,
       dense_rank() over (partition BY CId
                          ORDER BY score DESC)
FROM grade;
```

## 3. Find first two highest scores for each course.

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

## 4. Find students' total score, rank them. If tie, leave blank/ If tie, do consecutive ranking.

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

# SQL Logic Statement

## 1. Find The Following Data：

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

## 2. Find students's ID, name and average score for who dosen't pass two or more classes.

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


## 3. 统计各科成绩各分数段人数：课程编号，课程名称，[100-85]，[85-70]，[70-60]，[60-0] 及所占百分比

Find

```sql
select course.Cname,t1.*
from course LEFT JOIN (
select grade.CId,
	   CONCAT(round(sum(case when grade.score between 85 and 100 then 1 else 0 end )/count(*)*100,2),'%')
       as '[85-100]',
       CONCAT(round(sum(case when grade.score between 70 and 85 then 1 else 0 end )/count(*)*100,2),'%')
       as '[70-85)',
       CONCAT(round(sum(case when grade.score between 60 and 70 then 1 else 0 end )/count(*)*100,2),'%')
       as '[60-70)',
       CONCAT(round(sum(case when grade.score between 0 and 60 then 1 else 0 end )/count(*)*100,2),'%')
       as '[0-60)'
from grade
GROUP BY grade.CId) as t1 on course.CId=t1.CId
```

## 4. Count the number of students in each class (greater than 5 students)

```sql
select CId,
(case
when count(CId) > 5 then count(CId)
else 'not enough students'
end) as 'students_num'
from grade
group by CId;
```


12. 检索" 01 "课程分数小于 60，按分数降序排列的学生信息

select * from
(select GId, avg(score) as average
from grade
group by GId
order by average DESC) as tbl1 right join grade on (tbl1.GId = grade.GId)

13. 按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩

select * from
(select GId, avg(score) as average
from grade
group by GId
order by average DESC) as tbl1
right join grade on (tbl1.GId = grade.GId)

22. 查询名字中含有「风」字的学生信息

select * from student where SName like '%feng%'


24. 查询 1990 年出生的学生名单

select SId, SName, year(Sage) as born_year
from student
having born_year = '1990'

25. 查询每门课程的平均成绩，结果按平均成绩降序排列，平均成绩相同时，按课程编号升序排列

select grade.CId,
	avg(score) as grade_ave,
    course.Cname
from grade
     join course on grade.CId = course.CId
group by CId
order by grade_ave DESC, CId;

26. 查询平均成绩大于等于 85 的所有学生的学号、姓名和平均成绩

select grade.GId,
    student.Sname,
	round(avg(score),2) as grade_ave
from grade join student on grade.GId = student.SId
group by GId
having grade_ave >= 80
order by grade_ave DESC;


28. 查询所有学生的课程及分数情况（存在学生没成绩，没选课的情况）

select * from student s1
join grade g1 on s1.SId = g1.GId
join course c1 on g1.CId = c1.CId

29. 查询任何一门课程成绩在 70 分以上的姓名、课程名称和分数

select g1.GId, s1.SName, g1.score, c1.Cname
from grade g1
join student s1 on (g1.GId = s1.SId)
join course c1 on (g1.CId = c1.CId)
where score > 70

30. 查询不及格的课程

select s1.Sname, c1.Cname, g1.score from grade g1
         join student s1 on g1.GId = s1.SId
         join course c1 on g1.CId = c1.CId
where score <= 60

31. 查询课程编号为 01 且课程成绩在 80 分以上的学生的学号和姓名

select s1.SId, s1.SName
from grade g1 join student s1 on (g1.GId = s1.SId)
where score >= 80
and CId= '01';

27. 查询课程名称为「数学」，且分数低于 60 的学生姓名和分数

select Sname, score from student s1
join grade g1 on(s1.SId = g1.GId)
where CId = (select CId from course where Cname = 'shuxue')
and score < 60

32. 求每门课程的学生人数

select CId,
count(CId) as 'students_num'
from grade
group by CId;


35. 查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩

select distinct s1.Sname, g1.GId, g1.CId, g1.score
from grade g1
inner join grade g2 on g1.GId = g2.GId
inner join student s1 on g1.GId = s1.SId
where g1.CId != g2.CId
and g1.score = g2.score;

33. 成绩不重复，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩

select student.*,grade.score
from student ,course ,teacher ,grade
where course.CId=grade.CId
and course.TId=teacher.TId
and teacher.Tname='zhangsan'
and student.SId =grade.GId
order by grade.GId
LIMIT 1

34. 成绩有重复的情况下，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩

Should be very similar to the previous two



38. 检索至少选修两门课程的学生学号

select SId, Sname from student join(
select GId,
count(GId) as num_courses
from grade
group by GId
having num_courses >= 2
) tbl
on (student.SId = tbl.GId)

39. 查询选修了全部课程的学生信息

select * from student where SId in
(select GId
from grade
group by GId
having count(GId) = (select count(*) from course))

40. 查询各学生的年龄，只按年份来算

select Sname, year(curdate()) - year(Sage)  as age
from student;

41. 按照出生日期来算，当前月日 < 出生年月的月日则，年龄减一

select Sname, round(DATEDIFF(curdate(), SAge)/365,0)  as age from student;

42. 查询本周过生日的学生

select *
from student
where YEARWEEK(student.Sage)=YEARWEEK(CURDATE())

43. 查询下周过生日的学生

select *
from student
where YEARWEEK(student.Sage)=YEARWEEK(CURDATE()) + 1

44. 查询本月过生日的学生

select *
from student
where month(student.Sage)=month(CURDATE())

45. 查询下月过生日的学生

select *
from student
where month(student.Sage)=month(CURDATE()) + 1
