# Problem
Given a Weather table, write a SQL query to find all dates' Ids with higher temperature compared to its previous (yesterday's) dates.

# Create Table
```sql
Create table If Not Exists Weather (Id int, RecordDate date, Temperature int);
Truncate table Weather;
insert into Weather (Id, RecordDate, Temperature) values ('1', '2015-01-01', '10');
insert into Weather (Id, RecordDate, Temperature) values ('2', '2015-01-02', '25');
insert into Weather (Id, RecordDate, Temperature) values ('3', '2015-01-03', '20');
insert into Weather (Id, RecordDate, Temperature) values ('4', '2015-01-04', '30');
```

# Solution

Logic: Use self join again. Also, join based on the ID difference is 1 and today's temperature is higher than yesterday's temperature.

```sql
SELECT w2.Id
FROM Weather w1
JOIN Weather w2
WHERE DATEDIFF(w2.RecordDate,w1.RecordDate) = 1
  AND w1.Temperature < w2.Temperature
```
