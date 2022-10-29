import requests, json

from functions import url,getRecord
from getStockSymbols import getStockSymbols

def getCustomerStocks(serviceName = 'getCustomerStocks',userID = '',PIN = '',OTP = '999999'):
    #Header
    serviceName = 'getCustomerStocks'
    
    headerObj = {
        'Header': {
            'serviceName': serviceName,
            'userID': userID,
            'PIN': PIN,
            'OTP':OTP
        }
    }
    
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    if errorCode == '010000':
        depository_list = response.json()['Content']['ServiceResponse']['DepositoryList']
        return depository_list       


# getCustomerStocksFund(): Get all stocks owned by customer (including 0 quantity)

def getCustomerStocksFund(userID, PIN, OTP):
    #Header
    serviceName = 'getCustomerStocks'
    
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': userID,
                        'PIN': PIN,
                        'OTP':OTP
                        }
                        }
    
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    customer_portfolio = {}

    if errorCode == '010000':
        depository_list = response.json()['Content']['ServiceResponse']['DepositoryList']
        if depository_list == {}:
            print("No record found!")
        else:
            depository_list = depository_list['Depository']
            recordCount = getRecord(depository_list)
            if recordCount > 1:
                for i in range(0,recordCount,1):
                    depository = depository_list[i]
                    symbol_company = getStockSymbols(depository['symbol'])
                    # print("\nSymbol Name: {}".format(symbol_company))
                    # print("Quantity: {}".format(depository['quantity']))
                    # print("Price: {}".format(depository['price']))
                    # print("Trading Date: {}".format(depository['tradingDate']))
                    # print("Customer ID: {}".format(depository['customerID']))
                    
                    customer_portfolio[depository['symbol']] = {
                        'company': symbol_company,
                        'quantity': depository['quantity'],
                        'price': depository['price'],
                        'trading_date': depository['tradingDate'],
                        'customer_id': depository['customerID']
                    }

            elif recordCount == 0:
                    symbol_company = getStockSymbols(depository_list['symbol'])
                    # print("\nSymbol Name: {}".format(symbol_company))
                    # print("Quantity: {}".format(depository_list['quantity']))
                    # print("Price: {}".format(depository_list['price']))
                    # print("Trading Date: {}".format(depository_list['tradingDate']))
                    # print("Customer ID: {}".format(depository_list['customerID']))

                    customer_portfolio[depository['symbol']] = {
                        'company': symbol_company,
                        'quantity': depository_list['quantity'],
                        'price': depository_list['price'],
                        'trading_date': depository_list['tradingDate'],
                        'customer_id': depository_list['customerID']
                    }

    elif errorCode == '010041':
        print("OTP has expired.\nYou will receiving a SMS")
    else:
        print(serviceRespHeader['ErrorText'])

    return customer_portfolio