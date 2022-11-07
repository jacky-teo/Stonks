from urllib import response
import requests, json

from functions import url


def getStockHistory(serviceName = 'getStockHistory', userID = '',PIN = '',OTP = '9999', symbol='', numDays = ''):

   #Header
   serviceName = 'getStockHistory'

   #Content
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
                       'symbol': symbol,
                       'numDays' : numDays,
                       }
                       }

   final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
   response = requests.post(final_url)
   serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
   errorCode = serviceRespHeader['GlobalErrorID']
   if errorCode == '010000':

        stockHistory = response.json()['Content']['ServiceResponse']['Stock_History']

        stock_timeline = {
            symbol : json.loads("{}".format(stockHistory['jsonTimeSeries']).replace('\r', '').replace('\n', '')[:-5])
        }

        return stock_timeline

   elif errorCode == '010041':
       print("OTP has expired.\nYou will receiving a SMS")
   else:
       print(serviceRespHeader['ErrorText'])
getStockHistory()