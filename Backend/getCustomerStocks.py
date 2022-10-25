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
