import click
from datetime import datetime
from typing import Optional
from src.utils.mktcli_utils import *


@click.group()
def mktcli():
    pass


@mktcli.command(name='price')
@click.argument('labels', nargs=-1)
@click.option('-d', '--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), required=False)
@click.option('-c', '--currency', type=str, default=None, required=False)
def get_stock_price(labels: List[str], currency: Optional[str], date: str):
    """
    Retrieves and displays stock prices for the specified labels on a given date.

    This command-line function fetches the closing prices of specified stock tickers on a provided date,
    optionally converting them into a specified currency. If the given date falls on non-business day, the function
    exits with an error message.

    Args:
        labels (List[str]): One or more stock ticker symbols to retrieve prices for.
        currency (Optional[str]): A three-letter ISO currency code (e.g., 'EUR', 'GBP') for currency conversion.
                                  If not specified, prices remain in the original currency (USD).
        date (str): The date for which to retrieve stock prices, in 'YYYY-MM-DD' format. Defaults to the
                    current date.

    Returns:
        None: Outputs the DataFrame directly to the console.

    Example:
        mktcli price AAPL META -d 2024-12-23 -c EUR
    """
    if not check_business_date(date):
        click.echo(f'Date {date} is not valid business day, try again.')
        return

    stocks = get_latest_stocks_prices(labels=labels, date=date)

    if currency:
        try:
            rate = get_rate(currency=currency)
            stocks = {k: [v[0] * rate] for k, v in stocks.items()}
        except IndexError:
            click.echo('Currency non available for currency conversion, try again with different')
            return

    df = construct_dataframe(stocks, date=date)
    click.echo(df)
