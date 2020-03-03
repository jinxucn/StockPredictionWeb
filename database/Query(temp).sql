-- !preview conn=DBI::dbConnect(RSQLite::SQLite())

Query 1
select stock_name.stock_name, real_time.open
from stock_name join real_time on (stock_name.stock_ID = real_time.stock_ID)
order by minute desc limit 10;


Query 2
select stock_name.stock_name, max(history_day.high)
from stock_name join history_day on (stock_name.stock_ID = history_day.stock_ID)
group by stock_name.stock_name;


Query 3
select stock_name.stock_name, avg(history_day.high)
from stock_name join history_day on (stock_name.stock_ID = history_day.stock_ID)
where day between ()
group by stock_name.stock_name;


Query 4
select stock_name.stock_name, min(history_day.low)
from stock_name join history_day on (stock_name.stock_ID = history_day.stock_ID)
where day between ()
group by stock_name.stock_name;


Query 5
select a.stock_ID, a.stock_name
from stock_name a join history_day on (stock_name.stock_ID = history_day.stock_ID)
where avg(history_day.close) < (select min(history_day.low)
                                from stock_name b 
                                where b.day between() and b.stock_id = )
group by a.stock_ID