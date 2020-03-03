# Stocks Spider

A spider application for crawling stock historical and real-time data from the Internet

## Dependency

Install  **requests**:

```
>pip install requests
```

## Usage

By default, this program collects stock data of Google, Intel, Nvida, AMD, Alibaba, Coca-cola, Disney, Amazon, BiliBili, Netease.

For historical data:

```
>python crawlHistory.py
```

- Time period is from Feb-21-2019 to Feb-21-2020 GMT-5
- Two different intervals data: one-day and one-hour, which will be separately stored in *./data/1d/%StockSymbol%* and *./data/1h/%StockSymbol%*.

For real-time data:

```
>python crawlRealTime.py
```

- The initial time is Feb 26 2020, 13:20 GMT-5
- It crawls the data every minute, hour or day, depending on the current weekday and the hour
- Data would be store in *./data/1m/%StockSymbol​%*
