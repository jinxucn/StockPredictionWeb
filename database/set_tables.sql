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


#change some mistakes


alter table history_hour change hign high int;

alter table history_day change hign high int;

alter table real_time change hign high int;

#change timestamp to int;#change timestamp to int

alter table real_time modify minute int;

alter table history_day modify day int;

alter table history_hour modify hour int;


#create algorithm table and prediction table

create table algorithm
(algorithm_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
algorithm_name VARCHAR(40) NOT NULL)

insert into algorithm (algorithm_name)values
("POLY_BAYES") ,("SVM"), ("LSTM"), ("ARIMA")

create table pred_long
(
pred_time int,
stock_ID INT UNSIGNED,
algorithm_ID INT UNSIGNED AUTO_INCREMENT,
time_stamp int,
pred_value float,
PRIMARY KEY(pred_time, stock_ID, algorithm_ID, time_stamp),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID),
FOREIGN KEY(algorithm_ID) REFERENCES algorithm(algorithm_ID)
)

create table pred_short
(
pred_time int,
stock_ID INT UNSIGNED,
algorithm_ID INT UNSIGNED AUTO_INCREMENT,
time_stamp int,
pred_value float,
PRIMARY KEY(pred_time, stock_ID, algorithm_ID, time_stamp),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID),
FOREIGN KEY(algorithm_ID) REFERENCES algorithm(algorithm_ID)
)

create table indicator
(
stock_ID INT UNSIGNED,
time_stamp int,
pred_time int,
MACD float,
boll_up float,
boll_mid float,
boll_low float, 
PRIMARY KEY(pred_time, stock_ID, time_stamp),
FOREIGN KEY(stock_ID) REFERENCES stock_name(stock_ID)
)

