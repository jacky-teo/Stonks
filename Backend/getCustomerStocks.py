import requests, json

from functions import url,getRecord
from getStockSymbols import getStockSymbols

def getCustomerStocks(serviceName = 'getCustomerStocks',userID = '',PIN = '',OTP = '999999'):
    #Header
    serviceName = 'getCustomerStocks'
    userID = 'Z312312'
    PIN = '148986'
    OTP = '999999'
    
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
    #     if depository_list == {}:
    #         print("No record found!")
    #     else:
    #         depository_list = depository_list['Depository']
    #         recordCount = getRecord(depository_list)
    #         if recordCount > 1:
    #             for i in range(0,recordCount,1):
    #                 depository = depository_list[i]
    #                 symbol_company = getStockSymbols(depository['symbol'])
    #                 print("\nSymbol Name: {}".format(symbol_company))
    #                 print("Quantity: {}".format(depository['quantity']))
    #                 print("Price: {}".format(depository['price']))
    #                 print("Trading Date: {}".format(depository['tradingDate']))
    #                 print("Customer ID: {}".format(depository['customerID']))

                    
    #         elif recordCount == 0:
    #                 symbol_company = getStockSymbols(depository_list['symbol'])
    #                 print("\nSymbol Name: {}".format(symbol_company))
    #                 print("Quantity: {}".format(depository_list['quantity']))
    #                 print("Price: {}".format(depository_list['price']))
    #                 print("Trading Date: {}".format(depository_list['tradingDate']))
    #                 print("Customer ID: {}".format(depository_list['customerID']))
                    
    # elif errorCode == '010041':
    #     print("OTP has expired.\nYou will receiving a SMS")
    # else:
    #     print(serviceRespHeader['ErrorText'])

getCustomerStocks()         
