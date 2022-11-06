import requests, json
from functions import url
from getCustomerDetails import getCustomerDetails

def sendSMS(userID, PIN, message):
    #Header
    serviceName = 'sendSMS'
    userID = userID
    PIN = PIN
    OTP = '999999'
    #Content
    customerDetails = getCustomerDetails(userID, PIN)

    if customerDetails:
        mobileNumber = customerDetails['cellphone']['phoneNumber']
        # gender = customerDetails['profile']['gender']

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

