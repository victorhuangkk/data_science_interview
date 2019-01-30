# Problem
The Employee table holds all employees including their managers. Every employee has an Id, and there is also a column for the manager Id.
Given the Employee table, write a SQL query that finds out employees who earn more than their managers. For the above table, Joe is the only employee who earns more than his manager.

# Create Table
```sql
Create table If Not Exists Employee (Id int, Name varchar(255), Salary int, ManagerId int);
Truncate table Employee;
insert into Employee (Id, Name, Salary, ManagerId) values ('1', 'Joe', '70000', '3');
insert into Employee (Id, Name, Salary, ManagerId) values ('2', 'Henry', '80000', '4');
insert into Employee (Id, Name, Salary, ManagerId) values ('3', 'Sam', '60000', 'None');
insert into Employee (Id, Name, Salary, ManagerId) values ('4', 'Max', '90000', 'None');
```

# Solution

Logic: Since we have only one table, self join may be the only way to solve this problem. In this problem, the column ManagerId indicate wether the person is a manager or a pure employee.
1. Treat e1 as employee table
2. Treat e2 as manager table
3. Inner join those two tables to compare salaries. 

```sql
SELECT e1.Name AS 'Employee'
FROM Employee e1
JOIN Employee e2
  ON (e1.ManagerId = e2.Id)
  WHERE e1.Salary > e2.Salary;
```
