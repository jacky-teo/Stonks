import requests, json
from functions import url

def getStockPrice(serviceName = 'getStockPrice', userID = '',PIN = '',OTP = '999999', symbol=''):
    #Header
    serviceName = 'getStockPrice'
    
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
                        'symbol': symbol
                        }
                        }
    final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']
    
    if errorCode == '010000':
        stockDetail = response.json()['Content']['ServiceResponse']['Stock_Details']
        stock = {
            "Volume" : "{}".format(stockDetail['volume']),
            "Symbol" : "{}".format(stockDetail['symbol']),
            "Price"  : "{}".format(stockDetail['price']),
            "PercentageChange" : "{}".format(stockDetail['percentageChange']),
            "tradingDate" : "{}".format(stockDetail['tradingDate']),
            "change" : "{}".format(stockDetail['change']),
            "company" : "{}".format(stockDetail['company']),
            "prevClose" : "{}".format(stockDetail['prevClose']),
        }

        print(stock)
     
        return stock