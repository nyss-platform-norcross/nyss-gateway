#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import xmltodict
import requests
import json
import time
import datetime

API_URL = "http://ccce053a.ngrok.io/api/SmsGateway/"
MODEM_URL = "http://192.168.8.1/"
API_KEY = "7d956fc0-4a88-4600-88c1-aae478eca9b8"
INPUT_MESSAGE_FILE_PATH = "input_messages.txt"
OUTPUT_MESSAGE_FILE_PATH = "output_messages.txt"
ERROR_MESSAGE_FILE_PATH = "error_messages.txt"

HEADER_ACTION = MODEM_URL + "api/webserver/SesTokInfo"
NOTIFICATION_ACTION = MODEM_URL + "api/monitoring/check-notifications"
SMS_LIST_ACTION = MODEM_URL + "api/sms/sms-list"
DELETE_SMS_ACTION = MODEM_URL + "api/sms/delete-sms"
SEND_SMS_ACTION = MODEM_URL + "api/sms/send-sms"

SMS_LIST_TEMPLATE = '''<request>
    <PageIndex>1</PageIndex>
    <ReadCount>20</ReadCount>
    <BoxType>1</BoxType>
    <SortType>0</SortType>
    <Ascending>0</Ascending>
    <UnreadPreferred>0</UnreadPreferred>
    </request>'''

SMS_DEL_TEMPLATE = '<request><Index>{index}</Index></request>'

SMS_SEND_TEMPLATE = '''<request>
    <Index>-1</Index>
    <Phones><Phone>{phone}</Phone></Phones>
    <Sca></Sca>
    <Content>{content}</Content>
    <Length>{length}</Length>
    <Reserved>1</Reserved>
    <Date>{timestamp}</Date>
    </request>'''

def getHeaders():
    token = None
    sessionID = None
    try:
        r = requests.get(url=HEADER_ACTION)
    except requests.exceptions.RequestException as e:
        return (token, sessionID)
    try:        
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'TokInfo' in d['response']:
            token = d['response']['TokInfo']
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'SesInfo' in d['response']:
            sessionID = d['response']['SesInfo']
        return {'__RequestVerificationToken': token, 'Cookie': sessionID}
    except:
        pass
    return (token, sessionID)

def getUnreadMessageCount(headers):
    r = requests.get(url=NOTIFICATION_ACTION, headers=headers)
    d = xmltodict.parse(r.text, xml_attribs=True)
    count = int(d['response']['UnreadMessage'])
    return count

def getFirstUnreadMessage(headers):
    r = requests.post(url=SMS_LIST_ACTION, data=SMS_LIST_TEMPLATE, headers=headers)
    d = xmltodict.parse(r.text, xml_attribs=True)
    count = int(d['response']['Count'])
    data = d['response']['Messages']['Message']
    if count == 1:
        temp = data
        data = [temp]
    message = {
        "index": data[0]['Index'],
        "content": data[0]['Content'],
        "phone": data[0]['Phone']
    }
    return message

def sendMessage(headers, apiData):
    print(apiData.json())
    jsonData = apiData.json()
    content = jsonData["feedbackMessage"];
    data = SMS_SEND_TEMPLATE.format(
        phone = jsonData["phoneNumber"],
        content = content,
        length = len(content),
        timestamp = datetime.date.today().strftime("%Y-%m-%d %T")
    )
    r = requests.post(url=SEND_SMS_ACTION, data=data, headers=headers)

def deleteMessage(headers, index):
    r = requests.post(url=DELETE_SMS_ACTION, data=SMS_DEL_TEMPLATE.format(index=index), headers=headers)

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