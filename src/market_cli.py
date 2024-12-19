import calendar

import click
import yfinance as yf


@click.group()
def mktcli():
    pass


@click.command(name='price')
@click.argument('label')
@click.option('-v',
              '--verbose',
              type=bool,
              required=False,
              help="Verbose data return, if True -> Ticker, Date, Open price, Current price")
@click.option('-d',
              '--date',
              type=str,
              required=False)
def get_stock_price(label: str, verbose: bool = False, date: str = None):

    if (day_number := (calendar.weekday(*[int(x) for x in date.split('-')]))) > 5:
        click.echo(f'Date {date} is not valid, day is number {day_number}th of the week. '
                   f'\nSaturdays and Sundays not allowed')
        return

    stock = yf.Ticker(label).history()

    if date:
        stock = stock.loc[lambda x: x.index == date]

    if verbose:
        click.echo(f"Ticker: {label} "
                   f"\nDate: {stock.index[-1].date().strftime('%A, %d %b %Y')}"
                   f"\nOpen price: {float(stock.Open.iloc[-1])} "
                   f"\nCurrent price: {float(stock.Close.iloc[-1])}")
        return

    click.echo(f"Current price: {float(stock.Close.iloc[-1])}")


pycli.add_command(get_stock_price)
