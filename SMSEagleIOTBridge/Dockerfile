FROM docker.io/library/python:3.6.5-slim

RUN pip3 --no-cache install -U pip setuptools wheel

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache -r requirements.txt

COPY nyssIotBridge.py ./nyssIotBridge.py
COPY smsEagle-iot-hub-handler.py ./smsEagle-iot-hub-handler.py

CMD ["python", "smsEagle-iot-hub-handler.py"]
