import huaweiaccess
import sim868WaveshareAccess
import os



MOCK_STICK = -1
HUAWEI_LTE_STICK = 0
SIM868_WAVESHARE_GSM = 1

if os.get('GSM_STICK') is None:
    GSM_MODULE = MOCK_STICK
else:
    try:
        GSM_MODULE = int(os.get('GSM_STICK'))
    except Exception:
        print("Enviornment Variable GSM_STICK must be -1,0,1!!!")




def isPinRequired():
    if GSM_MODULE is HUAWEI_LTE_STICK:
        return huaweiaccess.isPinRequired()
    elif GSM_MODULE is SIM868_WAVESHARE_GSM:
        raise RuntimeError("Not Implemented")
    elif GSM_MODULE is MOCK_STICK:
        return True

def unlockWithPin(pin):
    if GSM_MODULE is HUAWEI_LTE_STICK:
        return huaweiaccess.unlockWithPin(pin)
    elif GSM_MODULE is SIM868_WAVESHARE_GSM:
        raise RuntimeError("Not Implemented")
    elif GSM_MODULE is MOCK_STICK:
        if pin == 5252:
            return True
        else:
            return False
