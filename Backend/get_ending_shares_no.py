# get_ending_shares_no(): Get the ending amount of shares to own depending on allocation & total investment amount
def get_ending_shares_no(total_invest, allocation, price):
    '''
        Takes in the following inputs:
            - Total Fund Investment Amount in SGD                           [Integer]       (e.g. 1000)
            - Stocks (Ticker) with its Allocation Percentage in the fund    [Dictionary]    (e.g. { "GOOG": 0.4, "D05.SI": 0.4, "S68.SI": 0.2 })
            - Price of each Stock in SGD                                    [Dictionary]    (e.g. { "GOOG": 103.485, "D05.SI": 32.76, "S68.SI": 8.35 })
        and outputs:
            - Number of shares to own for each stock                        [Dictionary]    (e.g. { "GOOG": 3, "D05.SI": 12, "S68.SI": 23 })
    '''
    ending_shares = {}

    for ticker in allocation:
        ticker_price = price[ticker]
        ticker_allocation = float(allocation[ticker])
        dollar_allocated = ticker_allocation * float(total_invest)
        quantity = int(dollar_allocated/ticker_price)
        ending_shares[ticker] = quantity

    print("Ending Shares:", ending_shares)
    return ending_shares