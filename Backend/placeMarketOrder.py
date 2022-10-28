import requests, json
from functions import url

# placeMarketOrder(): Place market order for buying or selling a single stock on tBank
def placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP):
    '''
        Takes in the following inputs:
            - userID                [String]
            - PIN                   [String]
            - settlementAccount     [String]
            - buyOrSell             [String]
            - symbol                [String]
            - quantity              [String]
            - OTP                   [String]
        and outputs:
            - Message/Response      [String]
    '''
    #Header
    serviceName = 'placeMarketOrder'
    
    headerObj = {
        'Header': {
            'serviceName': serviceName,
            'userID': userID,
            'PIN': PIN,
            'OTP': OTP
        }
    }
    contentObj = {
        'Content': {
            'settlementAccount': settlementAccount,
            'symbol': symbol,
            'buyOrSell': buyOrSell,
            'quantity': quantity
        }
    }
    final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']
    
    if errorCode == '010000':
        marketOrder = response.json()['Content']['ServiceResponse']['StockOrder']
        return "You have successfully placed a market order. The order ID is {}.".format(marketOrder['orderID'])

    elif errorCode == '010041':
        return "OTP has expired.\nYou will receiving a SMS"
    else:
        return serviceRespHeader['ErrorText']