import calendar
import click
import yfinance as yf
from typing import List
from datetime import date as dt


@click.group()
def mktcli():
    pass


@mktcli.command(name='price')
@click.argument('labels', nargs=-1)
@click.option('-v',
              '--verbose',
              type=bool,
              required=False,
              default=False,
              help="Verbose data return, if True -> Ticker, Date, Open price, Current price")
@click.option('-d',
              '--date',
              type=str,
              default=dt.today().strftime('%Y-%m-%d'),
              required=False)
def get_stock_price(labels: List[str],
                    verbose: bool,
                    date: str):
    if (day_number := check_business_date(date)) > 5:
        click.echo(f'Date {date} is not valid, day is number {day_number}th of the week. '
                   f'\nSaturdays and Sundays not allowed')
        return

    stocks = {ticker: yf.Ticker(ticker).history() for ticker in labels}
    stocks = {ticker: stock.loc[lambda x: x.index == date] for ticker, stock in stocks.items()}

    if verbose:
        for label, stock in stocks.items():
            click.echo(f"Ticker: {label} "
                       f"\nDate: {stock.index[-1].date().strftime('%A, %d %b %Y')}"
                       f"\nOpen price: {float(stock.Open.iloc[-1])} "
                       f"\nCurrent price: {float(stock.Close.iloc[-1])}")

        return

    for stock in stocks.values():
        click.echo(f"Current price: {float(stock.Close.iloc[-1])}")


def check_business_date(date: str):
    return calendar.weekday(*[int(x) for x in date.split('-')])
