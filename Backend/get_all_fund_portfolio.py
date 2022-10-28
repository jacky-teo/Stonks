from place_market_order import getCustomerStocks

# get_all_fund_portfolio(): Get all customer stocks details which is in the fund
def get_all_fund_portfolio(userID, PIN, OTP, fund_stocks):
    fund_portfolio = {}

    customer_portfolio = getCustomerStocks(userID, PIN, OTP)

    for ticker in customer_portfolio:
        if ticker in fund_stocks:
            fund_portfolio[ticker] = customer_portfolio[ticker]

    return fund_portfolio