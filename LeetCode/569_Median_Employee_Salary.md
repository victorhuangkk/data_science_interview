# Problem
Write a SQL query to find the median salary of each company. Bonus points if you can solve it without using any built-in SQL functions.

# Create Table
```sql
Create table If Not Exists Employee (Id int, Company varchar(255), Salary int)
Truncate table Employee
insert into Employee (Id, Company, Salary) values ('1', 'A', '2341')
insert into Employee (Id, Company, Salary) values ('2', 'A', '341')
insert into Employee (Id, Company, Salary) values ('3', 'A', '15')
insert into Employee (Id, Company, Salary) values ('4', 'A', '15314')
insert into Employee (Id, Company, Salary) values ('5', 'A', '451')
insert into Employee (Id, Company, Salary) values ('6', 'A', '513')
insert into Employee (Id, Company, Salary) values ('7', 'B', '15')
insert into Employee (Id, Company, Salary) values ('8', 'B', '13')
insert into Employee (Id, Company, Salary) values ('9', 'B', '1154')
insert into Employee (Id, Company, Salary) values ('10', 'B', '1345')
insert into Employee (Id, Company, Salary) values ('11', 'B', '1221')
insert into Employee (Id, Company, Salary) values ('12', 'B', '234')
insert into Employee (Id, Company, Salary) values ('13', 'C', '2345')
insert into Employee (Id, Company, Salary) values ('14', 'C', '2645')
insert into Employee (Id, Company, Salary) values ('15', 'C', '2645')
insert into Employee (Id, Company, Salary) values ('16', 'C', '2652')
insert into Employee (Id, Company, Salary) values ('17', 'C', '65')
```


# Solution

Use self-defined variables to solve this problem. A little bi tricky here. 

```sql
SELECT
  sub.Id,
  sub.Company,
  sub.Salary
FROM (
    SELECT
        @rank := IF(@lastCompany = e.Company, @rank + 1, 1) as Rank,
        e.id,
        e.company,
        e.salary,
        fre.tot,
        @lastCompany := e.company
    FROM (SELECT @rank := 0, @lastCompany := 'A') SQLvars, Employee e
    LEFT JOIN ( SELECT e1.company, count(*) as tot FROM Employee e1 GROUP BY e1.company ) fre ON fre.company = e.company
    ORDER BY e.Company, e.Salary
) sub
WHERE sub.rank = sub.tot DIV 2 + 1 OR (sub.tot % 2 = 0 AND sub.rank = sub.tot DIV 2)
```
