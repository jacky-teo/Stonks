from getCustomerStocks import getCustomerStocksFund

# get_all_fund_portfolio(): Get all customer stocks details which is in the fund
def get_all_fund_portfolio(userID, PIN, OTP, fund_stocks):
    fund_portfolio = {}

    customer_portfolio = getCustomerStocksFund(userID, PIN, OTP)
    # print(customer_portfolio)

    for ticker in customer_portfolio:
        if ticker in fund_stocks:
            fund_portfolio[ticker] = customer_portfolio[ticker]

    return fund_portfolio