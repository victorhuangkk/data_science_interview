# Problem
Write a SQL query to find employees who have the highest salary in each of the departments. For the above tables, Max has the highest salary in the IT department and Henry has the highest salary in the Sales department.


# Create Table
```sql
Create table If Not Exists Employee (Id int, Name varchar(255), Salary int, DepartmentId int);
Create table If Not Exists Department (Id int, Name varchar(255));
Truncate table Employee;
insert into Employee (Id, Name, Salary, DepartmentId) values ('1', 'Joe', '70000', '1');
insert into Employee (Id, Name, Salary, DepartmentId) values ('2', 'Henry', '80000', '2');
insert into Employee (Id, Name, Salary, DepartmentId) values ('3', 'Sam', '60000', '2');
insert into Employee (Id, Name, Salary, DepartmentId) values ('4', 'Max', '90000', '1');
Truncate table Department;
insert into Department (Id, Name) values ('1', 'IT');
insert into Department (Id, Name) values ('2', 'Sales');
```

# Solution

Logic: It is naturally use window function to rank. However, rank function dosen't support where clause. So, it needs to be selected as a temp table.

```sql
SELECT Department,
       Employee,
       Salary
FROM
  (SELECT Department.Name AS 'Department',
          Employee.Name AS 'Employee',
          rank() over (partition BY Employee.DepartmentId
                     ORDER BY Employee.Salary DESC) AS Num,
          Salary
   FROM Department
   JOIN Employee
     ON (Department.Id = Employee.DepartmentId)) AS temp
WHERE Num = 1;
```
