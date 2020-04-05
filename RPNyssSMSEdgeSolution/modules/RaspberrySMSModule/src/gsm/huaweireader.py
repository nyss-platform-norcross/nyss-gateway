import logging
import threading
import datetime
import uuid
import time
import xmltodict
import requests

from .services import GSMAdapter
from .model import RawSMS, GSMStatus

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


INPUT_MESSAGE_POSTFIX = "-input-message.txt"
MESSAGES_OUTBOX_FOLDER = "message-folder-outbox/"
MESSAGES_SENT_FOLDER = "message-folder-sent/"
MESSAGES_ERRORS_FOLDER = "message-folder-error/"

SMS_LIST_TEMPLATE = '''<request>
    <PageIndex>1</PageIndex>
    <ReadCount>1</ReadCount>
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

SMS_LIST_READ_TEMPLATE = '''<request>
    <PageIndex>1</PageIndex>
    <ReadCount>20</ReadCount>
    <BoxType>1</BoxType>
    <SortType>0</SortType>
    <Ascending>0</Ascending>
    <UnreadPreferred>1</UnreadPreferred>
    </request>'''


PIN_SET_TEMPLATE = '''
<request>
<OperateType>{}</OperateType>
<CurrentPin>{}</CurrentPin>
<NewPin>{}</NewPin>
<PukCode>{}</PukCode>
</request>
'''

SET_SMS_READ_TEMPLATE = '''
<request>
<Index>{}</Index>
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
SET_SMS_READ_ACTION = MODEM_URL + "api/sms/set-read"
GET_PROVIDER_NAME = MODEM_URL + "api/net/current-plmn"


class HuaweiSMS:

    def __init__(self, Phone, Date, Content, Index):
        self.Phone: str = Phone
        self.Date: str = Date
        self.Content: str = Content
        self.Index: str = Index


class HuaweiAdapter(GSMAdapter):
    def __init__(self, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log: logging.Logger = logger

        self.log.debug('Creating Huawei Reader')
        self.dummyThread = threading.Thread(
            name="Huawei SMS Reader", target=self._run, daemon=True)

        self._start()
        
        self._stick_found = False
        self._no_sim_card = True
        self._pin_required = True

    def _start(self):
        self.dummyThread.start()

    def _run(self):
        while True:
            try:
                if self._isSimCardInserted() is False:
                    self.log.debug('No Sim Card')
                    self._no_sim_card = True
                else:
                    self._no_sim_card = False
                if self._no_sim_card == False:
                    if self._isPinRequired() is False:
                        self._pin_required = False
                        break
                    self.log.debug('Waiting for pin unlock...')
            except:
                self.log.debug('Waiting for device availability')
            finally:
                time.sleep(5.)
        while True:
            try:
                status = self.getStatus()
                self._stick_found = True
                if status.available == False:
                    time.sleep(5)
                    self.log.debug('Waiting for network availability')
                    continue
                if len(self._smsHandler.keys()) == 0:
                    # no sms handler registered... don't do anything with the sms
                    time.sleep(5.)
                    continue
                for i in range(self._getUnreadMessageCount()):
                    if i > 20:
                        break
                    message = self._getFirstUnreadMessage()

                    if self._publishSMS(message):
                        self._handlePublishedSMS(message)

            except requests.ConnectionError:
                self._stick_found = False
                self.log.debug(
                    'Request Connection error... Stick is unreacheable')
            except:
                self._stick_found = False
                self.log.error(
                    "Unhandled Error in Huawei SMS reader loop!", exc_info=True)
            finally:
                time.sleep(5.)

    def isUnlocked(self) -> bool:
        return self._isPinRequired()

    def unlockWithPin(self, pin: str):
        return self._unlockWithPin(pin)

    def sendSMS(self, number: str, text: str, callback):
        self._sendMessage(number, text)
        callback()

    def getStatus(self) -> GSMStatus:

        try:
            if self._no_sim_card == True:
                status = GSMStatus(
                    signalStrength="Unavailable",
                    available="No sim card",
                    providerName="Unavailable"
                )
                return status
            if self._pin_required == True:
                status = GSMStatus(
                    signalStrength="Unavailable",
                    available="Pin Required",
                    providerName="Unavailable"
                )
                return status
            huaweiState = self._getState()
            if huaweiState['serviceAvailable']:
                available = "Yes"
            else:
                available = "No"

            status = GSMStatus(
                signalStrength="{}".format(huaweiState['signalStrength']),
                available=available,
                providerName=huaweiState['providerName'],
            )
            return status
        except requests.ConnectionError:
            if self._no_sim_card:
                status = GSMStatus(
                    signalStrength="Unavailable",
                    available="Stick not found",
                    providerName="Unavailable"
                )
                return status
            else:
                status = GSMStatus(
                    signalStrength="Unavailable",
                    available="Stick not found",
                    providerName="Unavailable"
                )
                return status

    def _publishSMS(self, message: HuaweiSMS):
        successful = True
        rawSms = RawSMS(message.Phone,
                        #  datetime.datetime.strptime(message.Date, '%Y-%m-%d %H:%M:%S'),
                        # TODO This currently uses the local utc timestamp!! dangerous
                        datetime.datetime.utcnow(),
                        message.Content)
        for handler in self._smsHandler.keys():
            try:
                self._smsHandler[handler](
                    rawSms)
            except:
                self.log.error(
                    'Exception in SMSHandler. Will not delete SMS and try again later', exc_info=True)
                successful = False

        return successful

    def _handlePublishedSMS(self, message: HuaweiSMS):
        try:
            self._deleteMessage(message)
        except:
            self.log.error(
                'Failed to delete message, trying to set it read. Careful - this may fill up the huawei stick with time', exc_info=True)
            try:
                self._setSmsRead(message)
            except:
                self.log.error(
                    'Failed to set SMS read after delete. Careful since this may bomb the API!')

    def _getHeaders(self):
        token = None
        sessionID = None
        try:
            r = requests.get(url=HEADER_ACTION, timeout=2.0)
        except requests.exceptions.RequestException as e:
            raise e
        try:
            d = xmltodict.parse(r.text, xml_attribs=True)
            if 'response' in d and 'TokInfo' in d['response']:
                token = d['response']['TokInfo']
            d = xmltodict.parse(r.text, xml_attribs=True)
            if 'response' in d and 'SesInfo' in d['response']:
                sessionID = d['response']['SesInfo']
            headers = {'__RequestVerificationToken': token,
                       'Cookie': sessionID}
        except:
            pass
        return headers

    def _disablePin(self, pin: str):
        d = self._postRequest(url=PIN_OPERATE_ACTION, data=PIN_SET_TEMPLATE.format(
            2, pin, '', ''))
        if d['response'] != "OK":
            raise IOError("Unexpected Response when disableing Pin")

    def _unlockWithPin(self, pin: str):
        d = self._postRequest(url=PIN_OPERATE_ACTION, data=PIN_SET_TEMPLATE.format(
            0, pin, '', ''))
        if d['response'] != "OK":
            raise IOError("Unexpected Response when unlocking with Pin")

    def _isPinRequired(self) -> bool:
        d = self._getRequest(url=PIN_STATUS_ACTION)
        if (d['response']['SimState']) == "260":
            return True
        else:
            return False

    def _isSimCardInserted(self) -> bool:
        d = self._getRequest(url=PIN_STATUS_ACTION)
        if (d['response']['SimState']) == "255":
            return False
        else:
            return True

    def _getUnreadMessageCount(self):
        d = self._getRequest(url=NOTIFICATION_ACTION)
        count = int(d['response']['UnreadMessage'])
        return count

    def _getFirstUnreadMessage(self) -> HuaweiSMS:
        d = self._postRequest(url=SMS_LIST_ACTION,
                              data=SMS_LIST_TEMPLATE)
        if (d['response']['Messages']['Message']):
            count = int(d['response']['Count'])
            data = d['response']['Messages']['Message']
            if count == 1:
                temp = data
                data = [temp]

            message = HuaweiSMS(Phone=data[0]['Phone'],
                                Date=data[0]['Date'],
                                Content=data[0]['Content'], Index=data[0]['Index'])
            # datetime.datetime.strptime(data[0]['Date'], '%Y-%m-%d %H:%M:%S')
        return message

    def _sendMessage(self, number: str, text: str):
        data = SMS_SEND_TEMPLATE.format(
            phone=number,
            content=text,
            length=len(text),
            timestamp=datetime.date.today().strftime("%Y-%m-%d %T")
        )
        d = self._postRequest(url=SEND_SMS_ACTION, data=data)

    def _deleteMessage(self, message: HuaweiSMS):
        d = self._postRequest(url=DELETE_SMS_ACTION, data=SMS_DEL_TEMPLATE.format(
            index=message.Index))
        if d['response'] != 'OK':
            raise IOError('Failed to delete message: {}'.format(message))

    def _getState(self):
        d = self._getRequest(MODEM_URL + 'api/monitoring/status')
        signalStrength = int(d['response']['SignalIcon'])
        if 'ServiceStatus' in d['response']:
            serviceStatus = int(d['response']['ServiceStatus'])
        else:
            serviceStatus = 0

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

        providerName = "Unkown"
        if serviceStatus == 2:
            d = self._getRequest(GET_PROVIDER_NAME)
            if 'FullName' in d['response']:
                providerName = d['response']['FullName']

        return {
            "signalStrength": signalStrength,
            "serviceAvailable": serviceStatus == 2,
            "networkType": networkTypeName,
            "providerName": providerName
        }

    def _setSmsRead(self, message: HuaweiSMS):
        data = SET_SMS_READ_TEMPLATE.format(
            message.Index
        )
        d = self._postRequest(SET_SMS_READ_ACTION, data)
        if d['response'] != 'OK':
            raise IOError(
                'Unexepected Response from Huawei Stick while setting SMS Read: {}'.format(d))

    def _postRequest(self, url, data) -> {}:
        r = requests.post(url=url, data=data,
                          headers=self._getHeaders(), timeout=2.0)
        return xmltodict.parse(r.text, xml_attribs=True)

    def _getRequest(self, url) -> {}:
        r = requests.get(url=url,
                         headers=self._getHeaders(), timeout=2.0)
        return xmltodict.parse(r.text, xml_attribs=True)


if __name__ == "__main__":
    logging.basicConfig()
    log = logging.getLogger('root')
    log.setLevel(logging.DEBUG)
    huawei = HuaweiAdapter(log)

    def handler(phone, text, date):
        print("Phone: {} - Texet: {} - Date: {}".format(phone, text, date))

    huawei.addSMSHandler(handler)

    while True:
        time.sleep(1.0)
