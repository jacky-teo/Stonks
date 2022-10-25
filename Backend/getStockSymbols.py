import requests, json
from functions import url

def getStockSymbols(symbol):
    serviceName = 'getStockSymbols'
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': '',
                        'PIN': '',
                        'OTP': ''
                        }
                        }
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)

    stockSymbols = response.json()['Content']['ServiceResponse']['StockSymbolList']['StockSymbol']
    Symbol_List= []
    Company_List = []
    
    for i in range(len(stockSymbols)):
        
        Symbol = stockSymbols[i]
        Symbol_List.append(Symbol['symbol'])
        Company_List.append(Symbol['company'])

    if symbol in Symbol_List:
        index = Symbol_List.index(symbol)
        return Company_List[index]
    else:
        return 'Record not found'



