## SQL 50 Problems.

# Please follow the commands here to create your own tables in for the SQL 50 Problems

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

# 1 Find when a student register both course '01' and course '02'.

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

# 2 Find entries whose course '01' has higher score than course '02'

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

# Remarks
The previous two queries funcion similarly. However, we always want to filter as early as possible. In marketing, this is calles marketing funnel.

# Find entries when course '01' exist but course '02' may not exist.

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

## Find entries when course '01' do not exist but course '02' exist.

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

## Find records with students who have score in grade table.

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

## Find students' info who have records in grade table.

Logic: Use subquery to select student's ID number in grade table. Add this condition as contraints in where predicates of the main query.

```sql
SELECT *
FROM student
WHERE SId in
    (SELECT distinct GId
     FROM grade);
```

## Find the number of teacher who's last name is 'li'.

```sql
select count(TId)
from teacher
where Tname like 'li%'
```

# Aggregate Functions

## Find records with average socre is at least 60 with students' info and average score.

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

## Find all students' ID, name, number of registered courses and total score for all courses (no score use null)

Logic: We used two tables in this example. Use student table to fetch all students' information and use grade table to select score that they get from every course.

```sql
select s1.*, total_courses, total_scores from
(select GId, count(score) as total_courses, sum(score) as total_scores
from grade
group by GId) as tbl1 right join student as s1
on (tbl1.GId = s1.SId);
```


# Window Function

## Rank by each course's score and show rank, Score ties are assigned the same rank, with the next ranking(s) skipped

 ```sql
select GId,
       score,
       rank() over (partition by CId order by score DESC)
from grade;
```


## Rank by each course's score and show rank, Score ties are assigned the same rank, with the consecutive ranking(s)

```sql
select GId,
       score,
       dense_rank() over (partition by CId order by score DESC)
from grade;
```

##  Find first two highest scores for each course.

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

6. 查询学过「张三」老师授课的同学的信息

select * from student where
SId in(
select GId from grade where CId =
(select CId from course where TId =
(select TId from teacher
where Tname = 'zhangsan')
));

7. 查询没有学全所有课程的同学的信息

select * from student
where SId not in
(select GId from grade
group by GId
having count(*) = (select count(CId) from course));

8. 查询至少有一门课与学号为" 01 "的同学所学相同的同学的信息

select * from student where SId in (
select distinct grade.GId from grade join
(select * from grade where GId = '01') as tmp
on (grade.CId = tmp.CId)
where grade.GId != '01'
);

9. 查询和" 01 "号的同学学习的课程 完全相同的其他同学的信息

select GId, sum(CId) from grade
where CId in (select CId from grade where GId = '01')
and GId != '01'
group by GId
having sum(CId) = (select sum(CId) from grade where GId = '01');

10. 查询没学过"张三"老师讲授的任一门课程的学生姓名

select SName from student
where SId not in
(select GId from grade where CId in (
select CId from course where TId in
(select TId from teacher where Tname = 'zhangsan'))
);

11. 查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩

select grade.GId, SName,
avg(score) as average
from grade join student where grade.GId = student.SId
group by grade.GId
having sum(
case
when score < 60 then 1
else 0
end ) >= 2

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

14. 查询各科成绩最高分、最低分和平均分：

以如下形式显示：课程 ID，课程 name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率

及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90

要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列

select g1.CId as courseID,
       c1.CName as courseName,
       MAX(g1.score)as max_score,
       MIN(g1.score)as min_score,
       AVG(g1.score)as ave_score,
       count(*)as register_num,
       sum(case when g1.score>=60 then 1 else 0 end )/count(*)as pass_rate,
       sum(case when g1.score between 70 and 80 then 1 else 0 end )/count(*)as 'C',
       sum(case when g1.score between 80 and 90 then 1 else 0 end )/count(*)as 'B',
       sum(case when g1.score>=90 then 1 else 0 end )/count(*)as 'A'
from grade as g1 join course c1 on (g1.CId = c1.CId)
GROUP BY g1.CId
ORDER BY count(*) DESC, g1.CId



16. 查询学生的总成绩，并进行排名，总分重复时保留名次空缺

select GId,
	   sum(score),
       rank() OVER (ORDER BY sum(score) DESC)
from grade
GROUP BY GId
ORDER BY sum(score) desc;

16.1 查询学生的总成绩，并进行排名，总分重复时不保留名次空缺

select GId,
	   sum(score),
       dense_rank() OVER (ORDER BY sum(score) DESC)
from grade
GROUP BY GId
ORDER BY sum(score) desc;

17. 统计各科成绩各分数段人数：课程编号，课程名称，[100-85]，[85-70]，[70-60]，[60-0] 及所占百分比

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

18. 查询各科成绩前三名的记录

select GId, grade_rank, score from
(select GId,
       CId,
       score,
       row_number() over (partition by CId order by score DESC) AS grade_rank
from grade) as temp
where grade_rank <= 3

19. 查询每门课程被选修的学生数

select CId, count(GId)
from grade
group by CId;

20. 查询出只选修两门课程的学生学号和姓名

select SId, Sname from student
where SId in
(select GId
from grade
group by GId
having count(CId) = 2);

21. 查询男生、女生人数

select Sgender, count(*) from student group by Sgender

22. 查询名字中含有「风」字的学生信息

select * from student where SName like '%feng%'

23. 查询同名同性学生名单，并统计同名人数

select * from student s1, student s2
where s1.SId != s2.SId and s1.SName = s2.SName

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

37. 统计每门课程的学生选修人数（超过 5 人的课程才统计）

select CId,
(case
when count(CId) > 5 then count(CId)
else 'not enough students'
end) as 'students_num'
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
