#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import xmltodict
import requests
import json
import time
import datetime
from huaweiaccess import *

API_URL = "http://ccce053a.ngrok.io/api/SmsGateway/"
API_KEY = "7d956fc0-4a88-4600-88c1-aae478eca9b8"
INPUT_MESSAGE_FILE_PATH = "input_messages.txt"
ERROR_MESSAGE_FILE_PATH = "error_messages.txt"


def sendToAPI(data):
    apiMessage = {
        "Sender": data["phone"],
        "TimeStamp": datetime.date.today().strftime("%Y%m%d%H%M%S"),
        "Text": data["content"],
        "MsgId": data["index"],
        "ApiKey": API_KEY,
        "Timezone": "TODO",
        "BinaryText": "TODO"
    }
    return requests.post(url = API_URL, json = apiMessage) 

def runSMSHandler():
    while True:
        time.sleep(3)

        #get input messages
        if getUnreadMessageCount(getHeaders()) != 0:
            message = getFirstUnreadMessage(getHeaders())
            with open(INPUT_MESSAGE_FILE_PATH, "a+") as file:
                file.write(json.dumps(message) + "\n");
            deleteMessage(getHeaders(), message['index'])

        #handle input messages
        with open(INPUT_MESSAGE_FILE_PATH, "r") as inputFile:
            rawMessage = inputFile.readline()
            while rawMessage:
                response = sendToAPI(json.loads(rawMessage))
                if (response.status_code == 200):
                    sendMessage(getHeaders(), response)
                else:
                    with open(ERROR_MESSAGE_FILE_PATH, "a+") as errorFile:
                        errorFile.write(rawMessage);
                rawMessage = inputFile.readline()
        
        #retreive unsend messages
        open(INPUT_MESSAGE_FILE_PATH, 'w').close()
        with open(ERROR_MESSAGE_FILE_PATH, "r") as errorFile:
            with open(INPUT_MESSAGE_FILE_PATH, "a+") as inputFile:
                line = errorFile.readline()
                while line:
                    inputFile.write(line);
                    line = errorFile.readline()
        open(ERROR_MESSAGE_FILE_PATH, 'w').close()
