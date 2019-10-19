#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import xmltodict
import requests
import json
import time
import datetime

API_URL = "http://7038467e.ngrok.io/api/SmsGateway/"
API_KEY = "oursupersecretapikey"
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

    open(INPUT_MESSAGE_FILE_PATH, 'w+')
    open(ERROR_MESSAGE_FILE_PATH, 'w+')
    while True:
        time.sleep(3)

        #get input messages
        if getUnreadMessageCount() != 0:
            message = getFirstUnreadMessage()
            with open(INPUT_MESSAGE_FILE_PATH, "a+") as file:
                file.write(json.dumps(message) + "\n");
            deleteMessage(message['index'])

        #handle input messages
        with open(INPUT_MESSAGE_FILE_PATH, "r") as inputFile:
            rawMessage = inputFile.readline()
            while rawMessage:
                response = sendToAPI(json.loads(rawMessage))
                if (response.status_code == 200):
                    sendMessage(response)
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
