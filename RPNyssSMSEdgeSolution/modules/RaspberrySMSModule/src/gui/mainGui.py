import tkinter
import tkinter.font
from functools import partial
import time
import raspberry
import subprocess
from gsm import GSMAdapter, GSMStatus



class PinEnterWindow:

    def __init__(self, gsmAdapter: GSMAdapter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = tkinter.Tk()
        self.baseFont = tkinter.font.Font(family="Arial", size=16)
        self.window.title("SMS Gateway")
        # self.window.geometry("600x400")
        self.window.attributes("-fullscreen", True)


        label = tkinter.Label(self.window, text="Pin Code Required")
        label.grid(row=0,columnspan=2, sticky="n")
        label.configure(font=self.baseFont)
        
        pinEntryLabel = tkinter.Label(self.window, text="Enter Pin:", font=self.baseFont)
        pinEntryLabel.grid(row=1, column=0, sticky="wn")


        self.pinTxt = tkinter.StringVar(self.window)
        pinEntry = tkinter.Entry(self.window, textvariable=self.pinTxt, font=self.baseFont)
        pinEntry.grid(row=1,column=1, sticky="enw")

        self.statusTxt = tkinter.StringVar(self.window)
        statusLabel = tkinter.Label(self.window, textvariable=self.statusTxt, font=self.baseFont, fg="red")
        statusLabel.grid(row=2,columnspan=2, sticky="enw")

        def submitPin():
            print(pinEntry.get())
            self.statusTxt.set("test")


        keyboard = tkinter.Frame(self.window)
        keyboard.grid(row=3, columnspan=2, sticky="new")
        keyboard.rowconfigure(1, weight=1)
        keyboard.columnconfigure(0, weight=1)
        keyboard.columnconfigure(1, weight=1)
        keyboard.columnconfigure(2, weight=1)

        def enterPin(nr):
            if len(self.pinTxt.get()) < 6:
                self.pinTxt.set(self.pinTxt.get() + str(nr))
                self.statusTxt.set("")
            else:
                self.statusTxt.set("Pin Code Length is limited to 6")

        def delete():
            if len(self.pinTxt.get()) > 0:
                self.pinTxt.set(self.pinTxt.get()[:-1])
        
        def submitPin():
            try:
                self.statusTxt.set("Submitting Pin...")
                result = gsmAdapter.unlockWithPin(int(self.pinTxt.get()))
                if result == False:
                    self.statusTxt.set("Pin Entry failed...")
                if result == True:
                    self.statusTxt.set("Sim Card Unlocked! ...")
                    self.window.after(3000, self.window.destroy)
            except Exception:
                self.statusTxt.set("Unknown Error...")


            


        tkinter.Button(keyboard, text="7", height=1, font=self.baseFont, command = partial(enterPin, 7)).grid(row=0, column = 0, sticky = "wne")
        tkinter.Button(keyboard, text="8", height=1, font=self.baseFont, command = partial(enterPin, 8)).grid(row=0, column = 1, sticky = "wne")
        tkinter.Button(keyboard, text="9", height=1, font=self.baseFont, command = partial(enterPin, 9)).grid(row=0, column = 2, sticky = "wne")
        tkinter.Button(keyboard, text="4", height=1, font=self.baseFont, command = partial(enterPin, 4)).grid(row=1, column = 0, sticky = "wne")
        tkinter.Button(keyboard, text="5", height=1, font=self.baseFont, command = partial(enterPin, 5)).grid(row=1, column = 1, sticky = "wne")
        tkinter.Button(keyboard, text="6", height=1, font=self.baseFont, command = partial(enterPin, 6)).grid(row=1, column = 2, sticky = "wne")
        tkinter.Button(keyboard, text="1", height=1, font=self.baseFont, command = partial(enterPin, 1)).grid(row=2, column = 0, sticky = "wne")
        tkinter.Button(keyboard, text="2", height=1, font=self.baseFont, command = partial(enterPin, 2)).grid(row=2, column = 1, sticky = "wne")
        tkinter.Button(keyboard, text="3", height=1, font=self.baseFont, command = partial(enterPin, 3)).grid(row=2, column = 2, sticky = "wne")
        tkinter.Button(keyboard, text="DEL", height=1, font=self.baseFont, command = delete).grid(row=3, column = 0, sticky = "wne")
        tkinter.Button(keyboard, text="0", height=1, font=self.baseFont, command = partial(enterPin, 0)).grid(row=3, column = 1, sticky = "wne")
        tkinter.Button(keyboard, text="OK", height=1, font=self.baseFont, command = submitPin).grid(row=3, column = 2, sticky = "wne")


        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.window.mainloop()




class StatusWindow:

    def __init__(self, gsmAdapter: GSMAdapter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = tkinter.Tk()
        # self.window.geometry("640x480")
        self.window.attributes("-fullscreen", True)
        self.ipTxt = tkinter.StringVar(self.window)
        self.gsmStateTxt = tkinter.StringVar(self.window)

        self.ipTxt.set("Checking...")
        self.gsmStateTxt.set("Checking...")
        def updateIpAddress():
            try:
                data = raspberry.rpistatus.getInterfaceStatus()
                self.ipTxt.set(data)
                self.window.after(1000, updateIpAddress)
            finally:
                pass
        
        def updateGSMState():
            try:
                # data = gsmadapter.getState()
                data: GSMStatus = gsmAdapter.getStatus()
                self.gsmStateTxt.set("Connected: {}\nSignal Strength: {}\nNetwork Type: {}".format(data.available, data.signalStrength, data.providerName))
                self.window.after(1000, updateGSMState)
            finally:
                pass

        self.window.after(1000, updateIpAddress)
        self.window.after(1000, updateGSMState)
        ipLlb = tkinter.Label(self.window, text="IP:").grid(row=0, column=0, sticky="nw")
        tkinter.Label(self.window, textvariable=self.ipTxt).grid(row=0, column=1, sticky="new")

        tkinter.Label(self.window, text="GSM:").grid(row=1, column=0, sticky="nw")
        tkinter.Label(self.window, textvariable=self.gsmStateTxt).grid(row=1,column=1, sticky="new")

        self.wifiHelp = tkinter.StringVar(self.window)
        self.wifiHelp.set("To Setup a WiFi Connection send a SMS with the following content to the Gateway:\n <SSID>:<Password>")

        tkinter.Label(self.window, textvariable=self.wifiHelp, wraplength=350).grid(row=2, column=0, columnspan=2, sticky="new")


        def shutdown():
            subprocess.call("sudo shutdown -h now", shell=True)

        tkinter.Button(self.window, text="Shutdown", command = shutdown).grid(row=3, column=0,columnspan=2, sticky="sew")

        
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.window.mainloop()



if __name__ == "__main__":
    window = StatusWindow()
