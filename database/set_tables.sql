-- !preview conn=DBI::dbConnect(RSQLite::SQLite())

create table stock_name
(stock_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
stock_name VARCHAR(40) NOT NULL)


create table history_day
(
stock_ID INT,
day TIMESTAMP,
open FLOAT,
close FLOAT,
volume FLOAT,
hign FLOAT,
low FLOAT,
PRIMARY KEY(stock_ID, day),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID)
)


create table history_hour
(
stock_ID INT UNSIGNED,
hour TIMESTAMP,
open FLOAT,
close FLOAT,
volume FLOAT,
hign FLOAT,
low FLOAT,
PRIMARY KEY(stock_ID, hour),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID)
)


create table real_time
(
stock_ID INT UNSIGNED,
minute TIMESTAMP,
open FLOAT,
close FLOAT,
volume FLOAT,
hign FLOAT,
low FLOAT,
PRIMARY KEY(stock_ID, minute),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID)
)
