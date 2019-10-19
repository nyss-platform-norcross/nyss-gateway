import http.server
import socketserver
from os import curdir, sep
import cgi
import json
import io
import threading
import huaweiaccess
import smsHandler
import time
import frontend
import gsmadapter

import logging


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('WebServer')
log.setLevel(logging.DEBUG)



PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

class myHandler(http.server.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.pinSet = False

    def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        if self.path=="/pinrequired":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if not huaweiaccess.isPinRequired():
                self.wfile.write(b'{"required": true}')
            else:
                self.wfile.write(b'{"required": false}')
            return
        if self.path=="/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"isGsm": true, "isInternet": true}')

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb') 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/pin":
            self.handlePin()


    def handlePin(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

           

        data = json.loads(self.data_string)
        pin = data['pin'].strip()
        if len(pin) != 4:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Pin Code length was not 4!')
            return
        try:
            pin = int(pin)
        except ValueError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Pin Code was not a number!')
            return
        
        try:
            if not huaweiaccess.isPinRequired():
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Pin Code Not Required!')
                return
            log.debug("Trying pin code {}".format(pin))

            if not huaweiaccess.unlockWithPin(pin):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Unlocking failed...')
                return
            if not huaweiaccess.disablePin(pin):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Disableing failed...')
                return

            self.send_response(200)
            self.end_headers()
            return
        except KeyboardInterrupt as keyErr:
            raise keyErr
        except Exception as err:
            log.debug("Exception while accessing Huawei LTE Stick", exc_info=True)
            self.send_response(503)
            self.end_headers()

def startHttpServer():
    log.debug("Starting http server!")
    with socketserver.TCPServer(("", PORT), myHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def startFronted():
    if gsmadapter.isPinRequired():
        frontend.PinEnterWindow()

def startSmsHandler():
    log.debug("Starting SMS Handler!")
    required = True
    count = 0
    while huaweiaccess.isPinRequired() or required:
    # while required:
        time.sleep(1)
        count = count + 1
        if count == 5:
            required = False
    log.debug("Entering SMS Handler loop")
    smsHandler.runSMSHandler()


# httpServer = threading.Thread(target=startHttpServer, daemon=True)
frontendThread = threading.Thread(target=startFronted, daemon=True)
smsHandlerThread = threading.Thread(target=startSmsHandler, daemon=True)

# httpServer.start()
frontendThread.start()
# smsHandlerThread.start()
# httpServer.join()
while True:
    try:
        time.sleep(1.)
    except KeyboardInterrupt as err:
        raise err

# if __name__ == "__main__":
    # log.debug('Starting SMS Gateway backend application')
