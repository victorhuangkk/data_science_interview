# Problem
Several friends at a cinema ticket office would like to reserve consecutive available seats.
Can you help to query all the consecutive available seats order by the seat_id using the following cinema table?
| seat_id | free |
|---------|------|
| 1       | 1    |
| 2       | 0    |
| 3       | 1    |
| 4       | 1    |
| 5       | 1    |

Your query should return the following result for the sample case above.
| seat_id |
|---------|
| 3       |
| 4       |
| 5       |

# Create Table
```sql
Create table If Not Exists cinema (seat_id int primary key auto_increment, free bool);
Truncate table cinema;
insert into cinema (seat_id, free) values ('1', '1');
insert into cinema (seat_id, free) values ('2', '0');
insert into cinema (seat_id, free) values ('3', '1');
insert into cinema (seat_id, free) values ('4', '1');
insert into cinema (seat_id, free) values ('5', '1');
```

# Solution
Logic: Use self join to find out consecutive availablity. Since SQL dosen't have for loop, these difference join trick is used to find consecutive values. 

```sql
SELECT distinct c1.seat_id
FROM cinema c1
JOIN cinema c2
  ON (c1.seat_id = c2.seat_id + 1
      OR c1.seat_id = c2.seat_id - 1)
WHERE c1.free = 1
  AND c2.free = 1
ORDER BY c1.seat_id
```
