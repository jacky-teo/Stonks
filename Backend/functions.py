import requests, json

def getRecord(record):
        try:
                recordCount = len(record);
                for i in range(0,recordCount,1):
                    acc = record[i]
                    return recordCount
        except KeyError:
                 if KeyError == 0:
                    recordCount = 1
                    return recordCount
                 else:
                    return 0


def url():
    return 'http://tbankonline.com/SMUtBank_API/Gateway'
