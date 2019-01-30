
# Problem
Write a SQL query to get the second highest salary from the Employee table.


# Create Table

```sql
Create table If Not Exists Employee (Id int, Salary int)
Truncate table Employee
insert into Employee (Id, Salary) values ('1', '100')
insert into Employee (Id, Salary) values ('2', '200')
insert into Employee (Id, Salary) values ('3', '300')
```


# Solution

Logic: We should use order by and limit to solve this problem. There are also several trivial points here.
1. use ifnull to handle corner case
2. select a temp table first, them select from this temp table to avoid error.
3. main idea is in the middle of this query. 

```sql
SELECT
    IFNULL(
      (SELECT DISTINCT Salary
       FROM Employee
       ORDER BY Salary DESC
        LIMIT 1 OFFSET 1),
    NULL) AS SecondHighestSalary

```
