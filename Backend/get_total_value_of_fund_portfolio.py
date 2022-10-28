# get_total_value_of_fund_portfolio():  Get the total value of the fund portfolio
def get_total_value_of_fund_portfolio(fund_portfolio):
    total = 0

    for ticker in fund_portfolio:
        price = float(fund_portfolio[ticker]['price'])
        quantity = float(fund_portfolio[ticker]['quantity'])
        total += price * quantity

    return total