
from .huaweireader import HuaweiAdapter
from .services import DummyAdapter, GSMAdapter
from .model import RawSMS

from common import MemberDecoratorClass

import datetime
import functools
import re
from re import Pattern

_isClassMethod: Pattern = re.compile(r'[.]+')
_SMS_LISTERNS = []


def SmsListener(func):

    
    global _SMS_LISTERNS
    if (_isClassMethod.search(func.__qualname__)):
        return MemberDecoratorClass(_SMS_LISTERNS, func)
    else:
        _SMS_LISTERNS.append(func)
        return func


def create_gsmadapter(reader_type: str, *args, **kwargs) -> GSMAdapter:
    adapter: GSMAdapter
    if reader_type == 'DUMMY':
        adapter = DummyAdapter(*args, **kwargs)
    elif reader_type == 'HUAWEI':
        adapter = HuaweiAdapter(**kwargs)
    else:
        raise ValueError('No Read defined by name: {}'.format(reader_type))

    for listener in _SMS_LISTERNS:
        adapter.addSMSHandler(listener)
