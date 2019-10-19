import time
import os
import json
import requests


API_URL = "http://7038467e.ngrok.io/api/SmsGateway/"
API_KEY = "oursupersecretapikey"
MESSAGES_FOLDER = "message-folder/"

def runSendToApiHandler():

    fileList = []

    while (True):
        time.sleep(1)
        if (len(fileList is not len([name for name in os.listdir('./' + MESSAGES_FOLDER)]))):
            fileList = [name for name in os.listdir('./' + MESSAGES_FOLDER)]
            getSmsAndPostToPlatform()

def getSmsAndPostToPlatform():
    smsDict = getLatestSmsDict()
    postSmsToPlatform(smsDict)

def getLatestSmsDict():
    fileNameLatestSms = sorted([name for name in os.listdir('./' + MESSAGES_FOLDER)])[-1] 
    with open(fileNameLatestSms, "r") as inputFile:
        rawMessage = inputFile.readline()
        return json.loads(rawMessage)


def postSmsToPlatform(smsDict):
    apiMessage = {
        "Sender": smsDict['sender'],
        "TimeStamp": smsDict['timestamp'],
        "Text": smsDict['text'],
        "MsgId": smsDict["gatewayId"],
        "ApiKey": API_KEY,
        "Timezone": "TODO",
        "BinaryText": "TODO"
    }
    return requests.post(url = API_URL, json = apiMessage)

# retreives SMS messages from a file for sending to the API
#def retreiveSMSMessage():
    #handle input messages
 #       with open(INPUT_MESSAGE_FILE_PATH, "r") as inputFile:
  #          rawMessage = inputFile.readline()
   #         while rawMessage:
    #            response = sendToAPI(json.loads(rawMessage))
     #           if (response.status_code == 200):
      #              sendMessage(response)
       #         else:
        #            with open(ERROR_MESSAGE_FILE_PATH, "a+") as errorFile:
         #               errorFile.write(rawMessage);
          #      rawMessage = inputFile.readline()