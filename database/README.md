About the database, we choose MySQL and set up 4 tables.

The “stock_name” table sets the “stock_id” as primary key and contains “stock_id” and stock_name.

The “history_day” table sets the “stock_id” together with “day” (timestamp) as primary keys and contains “open”, “close”, “high”, “low” and “volume”. And the “stock_id” is a foreign key from “stock_name” table.

The “history_hour” table sets the “stock_id” together with “hour” (timestamp) as primary keys and contains “open”, “close”, “high”, “low” and “volume”. And the “stock_id” is a foreign key from “stock_name” table.

The “real_time” table sets the “stock_id” together with “minute” (timestamp) as primary keys and contains “open”, “close”, “high”, “low” and “volume”. And the “stock_id” is a foreign key from “stock_name” table.

