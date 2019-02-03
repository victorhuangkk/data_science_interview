# Problem
Write a query to find the median of all numbers and name the result as median.

# Create Table
```sql
Create table If Not Exists Numbers (Number int, Frequency int);
Truncate table Numbers;
insert into Numbers (Number, Frequency) values ('0', '7');
insert into Numbers (Number, Frequency) values ('1', '1');
insert into Numbers (Number, Frequency) values ('2', '3');
insert into Numbers (Number, Frequency) values ('3', '1');
```


# Solution

Logic:   
(select sum(Frequency) from Numbers where Number<=n.Number) as left   
(select sum(Frequency) from Numbers where Number<=n.Number) as right   
Now if difference between Left and Right less or equal to Frequency of the current number that means this number is median.   
Ok, what if we get two numbers satisfied this condition? Easy peasy - take AVG().   


```sql
SELECT avg(n1.Number) AS median
FROM Numbers n1
WHERE n1.Frequency >= abs(
                            (SELECT sum(Frequency)
                             FROM Numbers
                             WHERE Number<=n1.Number) -
                            (SELECT sum(Frequency)
                             FROM Numbers
                             WHERE Number>=n1.Number))
```
