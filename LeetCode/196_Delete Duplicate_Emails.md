# Problem
Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its smallest Id.

# Create Table
| Id | Email     |
| :------------- | :------------- |
| 1       | john@example.com|
| 2       | bob@example.com|
| 3       | john@example.com |


After the query, final table becomes
| Id | Email     |
| :------------- | :------------- |
| 1       | john@example.com|
| 2       | bob@example.com|

# Solution

Logic: This is another scenorio to apply self join trick. But this time, it is asked to retain the smaller ID term. So, we need a condition to formulate this criteria. 

```sql
DELETE p1 FROM Person p1,
    Person p2
WHERE
    p1.Email = p2.Email AND p1.Id > p2.Id
```
