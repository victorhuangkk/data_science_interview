# Problem
Write a SQL query to rank scores. If there is a tie between two scores, both should have the same ranking. Note that after a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no "holes" between ranks.


# Create Table
```sql
Create table If Not Exists Scores (Id int, Score DECIMAL(3,2));
Truncate table Scores;
insert into Scores (Id, Score) values ('1', '3.5');
insert into Scores (Id, Score) values ('2', '3.65');
insert into Scores (Id, Score) values ('3', '4.0');
insert into Scores (Id, Score) values ('4', '3.85');
insert into Scores (Id, Score) values ('5', '4.0');
insert into Scores (Id, Score) values ('6', '3.65');
```

# Solution

Logic: Naturally, this problem should be solved by rank function. MySQL 5.7 support window function and Oracle/MS Server should support it too. Other than that, this question is easy.

```sql
SELECT Score,
       dense_rank() over (
                          ORDER BY Score DESC) AS 'Rank'
FROM Scores;
```
