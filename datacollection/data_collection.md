# Data Collection

This doc is about how to collect data.

## Structure

Data are collected following the steps (and uses modules):
1. Raw collection: `articles`, `finance`
1. Processing: `processor`
1. Provided: `provider`

Directory `pipeline` contains some script helping end-to-end data collection.

## Finance data

### API searching

I have investigated the following APIs:
* Google Finance API: it was deprecated on 2012. Future usage might be unstable. It is still currently functioning ([example](https://finance.google.com/finance/getprices?q=ACC&x=NSE&p=15&i=300&f=d,c,o,h,l,v), [example](https://finance.google.com/finance?q=AAPL,GOOG&output=json)). [Reference](http://www.jarloo.com/real-time-google-stock-api/).
* Yahoo Finance API: [recently discontinued](https://stackoverflow.com/questions/44048671/alternatives-to-the-yahoo-finance-api).
* [quandl](https://www.quandl.com/): this one is very promising providing historical data and "alternative data" (events that might affect trading strategy). However it costs about $50 per month.
* [intrinio](https://intrinio.com/): looks promising, investigated more (see below).
* [Alpha Vantage](https://www.alphavantage.co/): seems to be promising. The day-to-day [demo data](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo) seem to be what we need.

The two possible candidates are then Intrinio and Alpha Vantage. They are investigated, see below.

#### Intrinio

Registered with `chih.chiu.19@gmail` and using password `S*97`. Login and go to [account page](https://intrinio.com/account) to see the username and password used in API calls.

To see how to use its API to fetch data using `golang`, see `finance/intrinio`. The `finance/main` package has demo applications.

API reference: http://docs.intrinio.com/?javascript--api#data-point

#### Alpha Vantage

Registered for lifetime API key: `I9XIWDM97Z0LU2K0`.

Compared to Intrinio, Alpha Vantage is much easier to setup and can query the historical data of a stock fairly easily. See `finance/alphavantage` and `finance/main`.

API reference: https://www.alphavantage.co/documentation/

#### Comparison and conclusion

__Intrinio__
* (Pro) API-rich.
  - Able to fetch a list of US companies.
  - Able to fetch a tag from thousands of supported tags (`open_price` is one of the tag).
  - Able to specify the start and end date when querying daily prices.
* (Con) API has daily quota and 10-min quota, not sure what is the limit yet.
* (Con) Relatively hard to setup APIs to work.

__Alpha Vantage__
* (Pro) Easy to setup API.
* (Con) Can only query for "compact" and "full" data, which accounts for last 100 days or full 20 years of data.

For training data collection, we will use Intrinio to fetch all US companies, then use Alpha Vantage APIs to fetch all historical data for them.

For cron pipeline, either APIs seem to be fine.

### Web scraper

For reference we can also scrape webs, which can give us some bonus info. For example we can get finance news as well from the [Google Finance page](https://finance.google.com/finance?q=goog&ei=OSgbWsnBDIG02AaFhL-oCw). However scaper normally are tedious to develop, and since the gain is not clear at the moment, this as kept as an option but not investigated.

## Activity data

### API searching

I found the following API sources:
* [Event Registry](http://eventregistry.org/): this API can aggregate news into "events" for us, however the free tier can only search last month's events.
* [News API](https://newsapi.org/s/google-news-api): supports finding news since a given date. It didn't give any news older than a few months when I tried.
* [Aylien News API](https://aylien.com/news-api/): looks good but it is not free.
* [Webhose.io](https://webhose.io/): can access historical data as well as recent data. Free tier has 1K queries per month. Also not free when querying historical news.
* [Bing News Search](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-news-api-v7-reference): like Google APIs, looks very promising but [not free](https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-web-search-api).
* [NY Times](http://developer.nytimes.com/): providing a free API for querying articles back to 19xx.

I'll give News API and Webhose.io a try.

#### News API

Created API key `5d208cf6da6b4befaf6ba9984251efbf` with `chih.chiu.19@gmail` and password `S*97`. Usage can be seen from the [account page](https://newsapi.org/account).

Example:

```shell
curl https://newsapi.org/v2/everything -G -d q="google" -d from=2017-11-25 -d sortBy=popularity -d apiKey=5d208cf6da6b4befaf6ba9984251efbf
```

Another example (returns JSON):

```
https://newsapi.org/v2/everything?q=bitcoin&apiKey=5d208cf6da6b4befaf6ba9984251efbf
```

It is a GET-based JSON API, see more [here](https://newsapi.org/docs/get-started#search). Full doc [here](https://newsapi.org/docs).

The free tier [allows 1K queries per day](https://newsapi.org/pricing).

#### Webhost.io

Registered using `chih.chiu.19@gmail` with `S*97`. [This page](https://webhose.io/dashboard) includes API key, query generator, UI for building queries etc.

#### NY Times API

Registered using `chih.chiu.19@gmail` with no password, picked "article search" as the type. Gave `https://github.com/ChihChiu29/` as the required website. API key: `6e0d8a44a6df4fff92eaf3c53b913573`.

Example:

```
https://api.nytimes.com/svc/search/v2/articlesearch.json?q=google&begin_date=20140101&end_date=20140301&fl=web_url,lead_paragraph,snippet,abstract,headline,keywords,pub_date&page=3&api-key=6e0d8a44a6df4fff92eaf3c53b913573
```

Note that each response only has 10 results, and we need to use the "hits" and "offset" fields in the response to recursively get all results.

Check the full reference [here](http://developer.nytimes.com/article_search_v2.json#/Documentation/GET/articlesearch.json).

#### Comparison and conclusion

News API seems to be better purely based on that it allows more quries for the free tier. However for the prototype stage both are adequate, I pick News API for no strong reasons.
