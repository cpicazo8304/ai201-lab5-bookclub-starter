## Milestone 1 Notes
stats_service.py's all three functions are called in stats.py and each function uses get_reading_history that only gives books the user has finished, ordered by when they were started at (later started is first). However, just because you started later, doesn't mean you finished later.

Also, reading_streak not even used in the calculate_streak function.

HTTP request: http://127.0.0.1:5000/stats/USER_ID

## Milestone 2 Notes

### Alex's Stats

**reading_streak**: 0
**books_this_month**: 3
**total_pages_read**: 814

### Alex's history

There are three books Alex finished (two on 06-27-26 and one on 06-26-26), so there must be a reading_streak.

### Reading History function in routes/reading.py

It is promised that the most recently completed book will be first on the list, but the opposite happens when I request the information. Actually, it is ordered on most recent started date.

### Stats overview

The books_this_month and total_pages_read stats are correct, but the reading_streak is incorrect. Could be a bug in get_reading_history. However, if the function was wrong, then the other stats would be wrong. The only way the function could be wrong and have two of the stats be right is the fact that the two other stats don't care about order, but rather if the right books are included. reading_streak requires to read the order correctly, so calculate_streak must be doing something wrong. If the get_reading_history function was wrong, all three stats would be affected. Since only one stat is affected, the bug exists within the corresponding stat's function.

**Expected Streak:** 1