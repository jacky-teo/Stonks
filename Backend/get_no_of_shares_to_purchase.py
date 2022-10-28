# get_no_of_shares_to_purchase(): Get the number of shares to purchase each for a fund, based on the ending shares to own and the current shares in the fund
def get_no_of_shares_to_purchase(ending_shares, current_shares):
    '''
        Takes in the following inputs:
            - Quantity of ending stocks each        [Dictionary]    (e.g. { "GOOG": 3, "D05.SI": 12, "S68.SI": 23 })
            - Quantity of current stocks each       [Dictionary]    (e.g. { "GOOG": 2, "D05.SI": 0, "S68.SI": 250 })
        and outputs:
            - Quantity of stocks to purchase each   [Dictionary]    (e.g. { "GOOG": 1, "D05.SI": 12, "S68.SI": -227 })
    '''
    qty_purchase = {}

    for ticker in ending_shares:
        ending = ending_shares[ticker]
        starting = 0 if ticker not in current_shares else current_shares[ticker]
        to_purchase = ending - starting
        qty_purchase[ticker] = to_purchase

    print("How much to buy:", qty_purchase)
    return qty_purchase