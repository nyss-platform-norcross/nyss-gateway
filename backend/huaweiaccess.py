#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import requests
import json
import time
import datetime
# import sendEmail

MACRO_NET_WORK_TYPE_NOSERVICE = '0'          # /* 无服务            */
MACRO_NET_WORK_TYPE_GSM = '1'          # /* GSM模式           */
MACRO_NET_WORK_TYPE_GPRS = '2'          # /* GPRS模式          */
MACRO_NET_WORK_TYPE_EDGE = '3'          # /* EDGE模式          */
MACRO_NET_WORK_TYPE_WCDMA = '4'          # /* WCDMA模式         */
MACRO_NET_WORK_TYPE_HSDPA = '5'          # /* HSDPA模式         */
MACRO_NET_WORK_TYPE_HSUPA = '6'          # /* HSUPA模式         */
MACRO_NET_WORK_TYPE_HSPA = '7'          # /* HSPA模式          */
MACRO_NET_WORK_TYPE_TDSCDMA = '8'          # /* TDSCDMA模式       */
MACRO_NET_WORK_TYPE_HSPA_PLUS = '9'          # /* HSPA_PLUS模式     */
MACRO_NET_WORK_TYPE_EVDO_REV_0 = '10'         # /* EVDO_REV_0模式    */
MACRO_NET_WORK_TYPE_EVDO_REV_A = '11'         # /* EVDO_REV_A模式    */
MACRO_NET_WORK_TYPE_EVDO_REV_B = '12'         # /* EVDO_REV_A模式    */
MACRO_NET_WORK_TYPE_1xRTT = '13'         # /* 1xRTT模式         */
MACRO_NET_WORK_TYPE_UMB = '14'         # /* UMB模式           */
MACRO_NET_WORK_TYPE_1xEVDV = '15'         # /* 1xEVDV模式        */
MACRO_NET_WORK_TYPE_3xRTT = '16'         # /* 3xRTT模式         */
MACRO_NET_WORK_TYPE_HSPA_PLUS_64QAM = '17'         # /* HSPA+64QAM模式    */
MACRO_NET_WORK_TYPE_HSPA_PLUS_MIMO = '18'  # /* HSPA+MIMO模式     */
MACRO_NET_WORK_TYPE_LTE = '19'  # /*LTE 模式*/


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


PIN_SET_TEMPLATE = '''
<request>
<OperateType>{}</OperateType>
<CurrentPin>{}</CurrentPin>
<NewPin>{}</NewPin>
<PukCode>{}</PukCode>
</request>
'''

MODEM_URL = "http://192.168.8.1:80/"

INFORMATION_ACTION = MODEM_URL + "api/device/information"
HEADER_ACTION = MODEM_URL + "api/webserver/SesTokInfo"
NOTIFICATION_ACTION = MODEM_URL + "api/monitoring/check-notifications"
SMS_LIST_ACTION = MODEM_URL + "api/sms/sms-list"
DELETE_SMS_ACTION = MODEM_URL + "api/sms/delete-sms"
SEND_SMS_ACTION = MODEM_URL + "api/sms/send-sms"
PIN_OPERATE_ACTION = MODEM_URL + "api/pin/operate"
PIN_STATUS_ACTION = MODEM_URL + "api/pin/status"


def isDeviceReady():
    try:
        r = requests.get(url=INFORMATION_ACTION, timeout=(2.0, 2.0))
    except requests.exceptions.RequestException as e:
        return False

    if r.status_code != 200:
        return False
    return True


def isHilink(device_ip):
    try:
        r = requests.get(url=INFORMATION_ACTION, timeout=(2.0, 2.0))
    except requests.exceptions.RequestException as e:
        return False

    if r.status_code != 200:
        return False
    return True


def getHeaders():
    token = None
    sessionID = None
    try:
        r = requests.get(url=HEADER_ACTION)
    except requests.exceptions.RequestException as e:
        raise e
    try:
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'TokInfo' in d['response']:
            token = d['response']['TokInfo']
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'SesInfo' in d['response']:
            sessionID = d['response']['SesInfo']
        headers = {'__RequestVerificationToken': token, 'Cookie': sessionID}
    except:
        pass
    return headers


def disablePin(pin):
    r = requests.post(url=PIN_OPERATE_ACTION, data=PIN_SET_TEMPLATE.format(
        2, pin, '', ''), headers=getHeaders())
    d = xmltodict.parse(r.text, xml_attribs=True)
    if d['response'] != "OK":
        print("Unexpected Response when disableing Pin")
        print(d)
        return False
    else:
        return True


def unlockWithPin(pin):
    r = requests.post(url=PIN_OPERATE_ACTION, data=PIN_SET_TEMPLATE.format(
        0, pin, '', ''), headers=getHeaders())
    d = xmltodict.parse(r.text, xml_attribs=True)
    if d['response'] != "OK":
        print("Unexpected Response when unlocking with Pin")
        return False

    return disablePin(pin)


def isPinRequired():
    r = requests.get(url=PIN_STATUS_ACTION, headers=getHeaders())
    d = xmltodict.parse(r.text, xml_attribs=True)
    print(d)
    if (d['response']['SimState']) == "260":
        return True
    else:
        return False


def getUnreadMessageCount():
    r = requests.get(url=NOTIFICATION_ACTION, headers=getHeaders())
    d = xmltodict.parse(r.text, xml_attribs=True)
    count = int(d['response']['UnreadMessage'])
    return count


def getFirstUnreadMessage():
    r = requests.post(url=SMS_LIST_ACTION,
                      data=SMS_LIST_TEMPLATE, headers=getHeaders())
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


def sendMessage(apiData):
    print(apiData.json())
    jsonData = apiData.json()
    content = jsonData["feedbackMessage"]
    data = SMS_SEND_TEMPLATE.format(
        phone=jsonData["phoneNumber"],
        content=content,
        length=len(content),
        timestamp=datetime.date.today().strftime("%Y-%m-%d %T")
    )
    r = requests.post(url=SEND_SMS_ACTION, data=data, headers=getHeaders())


def deleteMessage(index):
    r = requests.post(url=DELETE_SMS_ACTION, data=SMS_DEL_TEMPLATE.format(
        index=index), headers=getHeaders())


def getState():
    r = requests.get(url=MODEM_URL + 'api/monitoring/status',
                     headers=getHeaders())
    d = xmltodict.parse(r.text, xml_attribs=True)
    signalStrength = int(d['response']['SignalIcon'])
    serviceStatus = int(d['response']['ServiceStatus'])

    networkType = int(d['response']['CurrentNetworkType'])
    networkTypeName = "None"
    if networkType is MACRO_NET_WORK_TYPE_LTE:
        networkTypeName = "LTE (4G)"
    elif networkType is MACRO_NET_WORK_TYPE_GSM:
        networkTypeName = "GSM (2G)"
    elif networkType is MACRO_NET_WORK_TYPE_GPRS:
        networkTypeName = "GPRS (2G)"
    elif networkType is MACRO_NET_WORK_TYPE_EDGE:
        networkTypeName = "EDGE (2G)"
    elif networkType is MACRO_NET_WORK_TYPE_1xRTT or networkType is MACRO_NET_WORK_TYPE_1xEVDV:
        networkTypeName = "RTT/EVDV (2G)"
    elif networkType is MACRO_NET_WORK_TYPE_NOSERVICE:
        networkTypeName = "No Service"
    else:
        networkTypeName = "(3G)"
    
    return {
        "signalStrength": signalStrength,
        "serviceAvailable": serviceStatus == 2,
        "networkType": networkTypeName
    }


if __name__ == "__main__":
    print(getState())
