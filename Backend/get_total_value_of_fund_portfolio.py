# get_total_value_of_fund_portfolio():  Get the total value of the fund portfolio
def get_total_value_of_fund_portfolio(fund_portfolio, price):
    total = 0

    for ticker in fund_portfolio:
        ticker_price = price[ticker]
        quantity = float(fund_portfolio[ticker]['quantity'])
        total += ticker_price * quantity

    return total