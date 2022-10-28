import requests

SUPPORTED_HTTP_METHODS = set(["GET","OPTIONS","HEAD","POST","PUT","PATCH","DELETE"])

def invoke_http(url, method='Get' , json=None, **kwargs):
    '''
    A simple wrapper for requests methods.
    url: the url of the http service
    method: method of http, default value Get
    json: the JSON input when needed, default value None
    return: A json data reply from the service
    '''
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            r = requests.request(method, url, json = json, **kwargs)
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
        
    if code not in range(200,300):
        return result

    ## Check http call result
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result
