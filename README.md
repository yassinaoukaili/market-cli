# Command Line Tool for Market Stock Prices

`market-cli` is a simple yet powerful command-line tool that allows you to retrieve live stock market prices and historical stock data. It also provides currency exchange rates to help convert stock prices to various currencies, making it a versatile tool for both stock tracking and financial analysis.

## Features

- **Retrieve Live Stock Prices**: Get the latest market prices for stocks.
- **Fetch Historical Stock Data**: Query stock prices for specific dates.
- **Currency Conversion**: Get real-time exchange rates for converting stock prices between different currencies.
  
## Installation

To install `market-cli`, follow these steps.

* #### Create your venv 

  Run command to create venv: 
  
  ```bash
  python -m venv venv
  ```
  Run command to activate venv:

  ```bash
  source venv/bin/activate
  ```
  (These commands may vary based on your OS)

* #### Clone the repository to you local machine

  Fork the repository to your own GitHub account by clicking the "Fork" button in the top-right corner, then clone the repository.

* #### Install mktcli and requirements

  To install, run the following command:
  
  ```bash
  pip install --editable . 
  ```

## Start fetching data 

To run `mkcli` and start fetching data:

```bash
mktcli price AAPL META GME
```
or 

```bash
mktcli price AAPL -d 2024-12-23 -c BTC 
```

#### Optional parameters:
* `-d`, `--date`: To specify a date. `mkcli` has internal checks to check if it is business day or not, in case of not business day will not return prices.
* `-c`, `--c`: To specify currency in case a price in diffent currency is needed. Supports all currencies and some cryptos (BTC, ETH etc..)




