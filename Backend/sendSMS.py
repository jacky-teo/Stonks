import requests, json
from functions import url
from getCustomerDetails import getCustomerDetails

def sendSMS():
    #Header
    serviceName = 'sendSMS'
    userID = ''
    PIN = ''
    OTP = ''
    #Content
    customerDetails = getCustomerDetails(userID, PIN)

    if customerDetails:
        mobileNumber = customerDetails['cellphone']['phoneNumber']
        gender = customerDetails['profile']['gender']

        if gender == 'M':
            message = 'Dear Mr. {}, your account has been credited with SGD1000.00'.format(customerDetails['familyName'])
        else:
            message = 'Dear Ms. {}, your account has been credited with SGD1000.00'.format(customerDetails['familyName'])
        # message = 'Hi, '
        
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
                            'mobileNumber': mobileNumber,
                            'message': message
                            }
                            }
        
        final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
        response = requests.post(final_url)
        serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
        errorCode = serviceRespHeader['GlobalErrorID']
        
        if errorCode == '010000':
            print("SMS sent")
        elif errorCode == '010041':
            print("OTP has expired.\nYou will receiving a SMS")
        else:
            print(serviceRespHeader['ErrorText'])

sendSMS()
