import os
import threading
from six.moves import input
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from azure.iot.device.exceptions import ConnectionFailedError
import json
import logging
import time

logger = logging.getLogger("iot-hub-bridge")


def _execute_command(method, payload):
    try:
        data = method(payload)
        return 200, data
    except Exception as e:
        return 400, str(e)


def device_method_listener(device_client, methods_to_listen_for):
    while True:
        method_request = device_client.receive_method_request()
        logger.debug("Incoming direct method '{}'\nPayload: {}".format(method_request.name, str(method_request.payload)))

        if method_request.name in methods_to_listen_for:
            status, data = _execute_command(methods_to_listen_for[method_request.name], method_request.payload)
        else:
            status, data = 404, "Direct method {} not defined".format(method_request.name)

        if status is 200:
            payload = {"isSuccess": True, "data": data}
        else:
            payload = {"isSuccess": False, "data": data}

        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        device_client.send_method_response(method_response)

def connect(client):
    print("Connecting to IoT Hub")
    try:
        client.connect()
    except ConnectionFailedError as e:
        print("Could not connect to IoT Hub")
        return False
    else:
        return True

def init(connection_string, methods):
    if connection_string is "":
        print("Missing connection string!")
        return 0

    client = IoTHubDeviceClient.create_from_connection_string(connection_string, websockets=True)
    # connect the client.
    while connect(client) == False:
        time.sleep(10)
    
    print("Starting listening for direct methods of type [{}]...".format(', '.join(methods.keys())))

    # Run method listener threads in the background
    device_method_thread = threading.Thread(target=device_method_listener, args=(client, methods))
    device_method_thread.daemon = True
    device_method_thread.start()
