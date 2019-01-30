# Problem
Write a SQL query to find all duplicate emails in a table named Person.


# Create Table
```sql
Create table If Not Exists Person (Id int, Email varchar(255));
Truncate table Person;
insert into Person (Id, Email) values ('1', 'a@b.com');
insert into Person (Id, Email) values ('2', 'c@d.com');
insert into Person (Id, Email) values ('3', 'a@b.com');
```

# Solution
Logic: Duplicate means the counting is larger than 1. For that reason, use aggregate function to calculate the count and filter this criteria by having. 

```sql
SELECT Email
FROM person
GROUP BY Email
HAVING count(Email) > 1
```
