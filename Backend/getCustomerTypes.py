import requests, json
from functions import url

def getCustomerTypes(customerID):
    serviceName = 'getCustomerTypes'
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

    customerType = response.json()['Content']['ServiceResponse']['CustomerTypeList']['CustomerType']
    ID_List= []
    Name_List = []
    
    for i in range(len(customerType)):
        customer = customerType[i]
        ID_List.append(customer['CustomerTypeID'])
        Name_List.append(customer['CustomerTypeName'])

    if customerID in ID_List:
        index = ID_List.index(customerID)
        return Name_List[index]
    else:
        return 'Record not found'
        

        
                   
                         


