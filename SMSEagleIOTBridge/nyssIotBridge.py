import os
import threading
from six.moves import input
from azure.iot.device import IoTHubDeviceClient, MethodResponse
import json
import logging

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


def init(connection_string, methods):
    if connection_string is "":
        print("Missing connection string!")
        return 0

    print("Starting listening for direct methods of type [{}]...".format(', '.join(methods.keys())))

    client = IoTHubDeviceClient.create_from_connection_string(connection_string, websockets=True)
    # connect the client.
    client.connect()

    # Run method listener threads in the background
    device_method_thread = threading.Thread(target=device_method_listener, args=(client, methods))
    device_method_thread.daemon = True
    device_method_thread.start()


if __name__ == "__main__":
    logging.basicConfig()
    if conn_str is "":
        print("You need to fill in the connection string at the top of the file.")
    #init(lambda x: print(x), conn_str)
    # Wait for user to indicate they are done listening for messages
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break
    _device_client.disconnect()
