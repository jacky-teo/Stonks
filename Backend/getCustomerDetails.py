import requests, json
from functions import url
from getCustomerTypes import getCustomerTypes

def getCustomerDetails(userID, PIN):
    #Header
    serviceName = 'getCustomerDetails'
    userID = userID
    PIN = PIN
    OTP = '999999'
    
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': userID,
                        'PIN': PIN,
                        'OTP': OTP
                        }
                        }
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']
    
    if errorCode == '010000':
        CDMCustomer = response.json()['Content']['ServiceResponse']['CDMCustomer']
        return CDMCustomer
            
    #     print('Date of Birth: {}'.format(CDMCustomer['dateOfBirth']))
    #     print('Tax Identifier: {}'.format(CDMCustomer['taxIdentifier']))
    #     print('Local Number: {}'.format(CDMCustomer['phone']['localNumber']))
    #     print('Area Code: {}'.format(CDMCustomer['phone']['areaCode']))
    #     print('Country Code: {}'.format(CDMCustomer['phone']['countryCode']))
    #     print('Certificate Issuer: {}'.format(CDMCustomer['certificate']['certificateIssuer']))
    #     print('Certificate No.: {}'.format(CDMCustomer['certificate']['certificateNo']))
    #     print('Certificate Expiry Date: {}'.format(CDMCustomer['certificate']['certificateExpiryDate']))
    #     print('Certificate Type: {}'.format(CDMCustomer['certificate']['certificateType']))
    #     print('Postal Code: {}'.format(CDMCustomer['address']['postalCode']))
    #     print('Street Address 1: {}'.format(CDMCustomer['address']['streetAddress1']))
    #     print('Street Address 2: {}'.format(CDMCustomer['address']['streetAddress2']))
    #     print('State: {}'.format(CDMCustomer['address']['state']))
    #     print('Country: {}'.format(CDMCustomer['address']['country']))
    #     print('City: {}'.format(CDMCustomer['address']['city']))
    #     print('Phone Number: {}'.format(CDMCustomer['cellphone']['phoneNumber']))
    #     print('Country Code: {}'.format(CDMCustomer['cellphone']['countryCode']))
    #     print('Family Name: {}'.format(CDMCustomer['familyName']))
    #     print('Registration Date: {}'.format(CDMCustomer['maintenacehistory']['registrationDate']))
    #     print('Last Maintenance Teller: {}'.format(CDMCustomer['maintenacehistory']['lastMaintenanceTellerId']))
    #     print('Given Name: {}'.format(CDMCustomer['givenName']))
    #     print('Customer ID: {}'.format(CDMCustomer['customer']['customerID']))
    #     print('isMerchant: {}'.format(CDMCustomer['profile']['isMerchant']))
    #     print('Occupation: {}'.format(CDMCustomer['profile']['occupation']))
    #     print('Fax: {}'.format(CDMCustomer['profile']['fax']))
    #     print('Nationality: {}'.format(CDMCustomer['profile']['nationality']))
    #     print('Customer Type: {}'.format(getCustomerTypes(CDMCustomer['profile']['customerType'])))
    #     print('Email: {}'.format(CDMCustomer['profile']['email']))
    #     print('Ethnic Group: {}'.format(CDMCustomer['profile']['ethnicGroup']))
    #     print('Gender: {}'.format(CDMCustomer['profile']['gender']))
    #     print('isBillingOrg: {}'.format(CDMCustomer['profile']['isBillingOrg']))
    #     print('Bank ID: {}'.format(CDMCustomer['profile']['bankID']))
    # elif errorCode == '010041':
    #     print("OTP has expired.\nYou will receiving a SMS") 
    # else:
    #     print(serviceRespHeader['ErrorText'])

