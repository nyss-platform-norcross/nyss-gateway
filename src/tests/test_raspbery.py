import unittest
import unittest.mock
from gsm import RawSMS
from raspberry.wifihandler import handleWifiSMS, _addNewWifiSettings
import raspberry.wifihandler


class TestWifiHandling(unittest.TestCase):

    @unittest.mock.patch('raspberry.wifihandler._addNewWifiSettings')
    def testCorrectSms(self, mock: unittest.mock.Mock):
        sms = RawSMS(None, None, 'WIFI:DasHier:allesgrossgschrieben')
        handleWifiSMS(sms)
        mock.assert_called_once_with('DasHier', 'allesgrossgschrieben')

    @unittest.mock.patch('raspberry.wifihandler._addNewWifiSettings')
    def testFalseSms(self, mock: unittest.mock.Mock):
        sms = RawSMS(None, None, '#34#25#3#')
        handleWifiSMS(sms)
        mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
