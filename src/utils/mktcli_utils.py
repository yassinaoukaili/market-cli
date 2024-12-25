import requests
import pandas as pd
import yfinance as yf
from typing import List
from bs4 import BeautifulSoup
import numpy as np


def check_business_date(date: str):
    """
    Checks if a given date falls on a weekday.

    Args:
        date (str): A string representing the date in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the date is a weekday (Monday to Friday), False if it is a weekend (Saturday or Sunday).
    """
    stock_market_closed_2025 = [
        '2025-01-01',  # New Year's Day
        '2025-01-20',  # Martin Luther King Jr. Day
        '2025-02-17',  # Presidents' Day
        '2025-04-20',  # Easter Sunday (Observed on Monday)
        '2025-05-26',  # Memorial Day
        '2025-06-19',  # Juneteenth National Independence Day
        '2025-07-04',  # Independence Day
        '2025-09-01',  # Labor Day
        '2025-10-13',  # Columbus Day
        '2025-11-11',  # Veterans Day
        '2025-11-27',  # Thanksgiving Day
        '2025-12-25',  # Christmas Day
        '2025-11-28',  # Thanksgiving Day (Early closure)
        '2025-12-24',  # Christmas Eve (Early closure)
    ]
    return np.is_busday([date], holidays=stock_market_closed_2025)[0]


def get_latest_stocks_prices(labels: List[str], date: str):
    """
    Retrieves the closing stock prices for a given list of stock tickers on a specific date.

    Args:
        labels (List[str]): A list of stock ticker symbols (e.g., ['AAPL', 'META', 'MSFT']).
        date (str): The specific date for which to retrieve the closing prices.

    Returns:
        dict: A dictionary where each key is a stock ticker, and the value is a list containing the
              closing price for the specified date.
    """

    stocks = {ticker: yf.Ticker(ticker).history().Close for ticker in labels}
    stocks = {ticker: [stock.loc[lambda x: x.index == date].iloc[0]] for ticker, stock in stocks.items()}
    return stocks


def construct_dataframe(stocks: dict, date: str):
    """
    Constructs a Pandas DataFrame from stock price data.

    Args:
        stocks (dict): A dictionary where keys are stock tickers and values are lists containing
                       stock prices (e.g., {'AAPL': [150.0], 'GOOG': [2800.0]}).
        date (str): The date to use as the index for the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with stock tickers as columns, stock prices as the data,
                      and the specified date as the index.
    """
    return pd.DataFrame.from_records(stocks, index=[date])


def parse_rates():
    """
    Fetches currency exchange rates from the XE website and processes the data into a Pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing currency exchange rates with columns corresponding
                      to the table headers on the XE website.
    """

    r = requests.get('https://www.xe.com/currencytables/?from=USD')
    html = BeautifulSoup(r.text, features='lxml')

    table = html.find('table', {'class': "sc-f2b5952d-3 hidSsf"})

    columns = table.find('thead').find_all('th')
    column_names = [x.text.strip() for x in columns]

    body = table.find('tbody')

    dict_currencies = {}
    for row in body.find_all('tr'):
        dict_currencies[row.find('th').text.strip()] = [x.text.strip() for x in row.find_all('td')]

    df = pd.DataFrame.from_dict(dict_currencies, orient='index') \
        .reset_index() \
        .set_axis(column_names, axis=1)

    return df


def get_rate(currency: str):
    """
     Retrieves the exchange rate for a specified currency.

     Args:
         currency (str): The three-letter ISO 4217 currency code (e.g., 'EUR' for Euro, 'JPY' for Japanese Yen).

     Returns:
         float: The exchange rate of the specified currency in terms of "Units per USD".
    """

    df_rates = parse_rates()
    rate = df_rates.loc[lambda x: x.Currency == currency]['Units per USD'].iloc[0]

    return float(rate)
