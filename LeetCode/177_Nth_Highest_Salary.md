# PRoblem
Write a SQL query to get the nth highest salary from the Employee table.


# Create Table
```sql
Create table If Not Exists Employee (Id int, Salary int)
Truncate table Employee
insert into Employee (Id, Salary) values ('1', '100')
insert into Employee (Id, Salary) values ('2', '200')
insert into Employee (Id, Salary) values ('3', '300')
```

# Solution

Logic: To handle this problem, we will naturally use order by combine with offset. In LeetCode exercise, we also need to handle corner case.

1. set N = N - 1 to redefine a variable
2. use ifnull to handle if no highest salary case.

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  set N=N-1;
RETURN (
ifnull((select distinct Salary from Employee
order by Salary desc
limit 1 offset N),null)
);
END
```
