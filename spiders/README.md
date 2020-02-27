# Stocks Spider

A spider application for crawling stock historical and real-time data from the Internet

## Dependency

Install  **requests**:

```
>pip install requests
```

## Usage

For historical data:

```
>python crawlHistory.py
```

- By default, it crawls stocks information from Feb-21-2019 to Feb-21-2020, the intervals are one-day and one-hour, which will be separately stored in *./data/1d/* and *./data/1h/*.

- By default, it collects stock of Nvida, AMD, Alibaba, Coca-cola, Disney, Amazon, BiliBili, Netease, Intel, and Nike.