
from .huaweireader import HuaweiAdapter
from .services import DummyAdapter, GSMAdapter

def create_gsmadapter(reader_type: str, *args, **kwargs) -> GSMAdapter:
    if reader_type == 'DUMMY':
        return DummyAdapter(*args, **kwargs)
    elif reader_type == 'HUAWEI':
        return HuaweiAdapter(**kwargs)

