import os
import threading
from six.moves import input
from azure.iot.device import IoTHubDeviceClient, MethodResponse
import json
import logging

def generic_callback(params):
    _log.debug("Callback with the following parameters is not supported or was not yet defined:" + str(params))

conn_str = ""
_device_client = None
_send_sms_callback = generic_callback
_log = logging.getLogger("iot-hub-bridge")


def register_sms_callback(sms_callback):
    global _send_sms_callback
    _send_sms_callback = sms_callback

def _execute_command(payload, callback):
    try:
        data = callback(payload)
        return 200, data
    except Exception as e:
        # log exception, handle any errors and return status code depending on error
        return 400, str(e)


def _handle_direct_method(method_name, method_callback):
    method_request = _device_client.receive_method_request(method_name)
    # TODO: check for bad payload e.g. payload = None, or params not cotrrect
    _log.debug("Params are:" + str(method_request.payload))
    status, data = _execute_command(method_request.payload, method_callback)
    if status is 200:
        payload = {"result": True, "data": data}
    else:
        payload = {"result": False, "data": data}

    method_response = MethodResponse.create_from_method_request(
        method_request, status, payload)
    _device_client.send_method_response(method_response)  # send response


def _send_sms():
    while True:
        _handle_direct_method("send_sms", _send_sms_callback)

def init(sms_callback, connection_string):
    conn_str = connection_string

    global _device_client
    # The client object is used to interact with your Azure IoT hub.
    _device_client = IoTHubDeviceClient.create_from_connection_string(
        conn_str, websockets=True)

    register_sms_callback(sms_callback)

    # connect the client.
    _device_client.connect()

    # Run method listener threads in the background
    handle_send_sms_thread = threading.Thread(
        target=_send_sms)
    handle_send_sms_thread.daemon = True
    handle_send_sms_thread.start()


def uninitialize():
    # finally, disconnect
    _device_client.disconnect()

def raiseValueError(x):
    raise ValueError(str(x))

if __name__ == "__main__":
    logging.basicConfig()
    if conn_str is "":
        print("You need to fill in the connection string at the top of the file.")
    init(lambda x: print(x), conn_str)
    # Wait for user to indicate they are done listening for messages
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break
    uninitialize()
