Raspberry Zero W Setup:

- install raspbian lite
- put ssh file in root of boot sd card
- put wpa_supplicant.conf file in root of boot sd card:

    country=us  
    update_config=1
    ctrl_interface=/var/run/wpa_supplicant

    network={
    ssid="<Name of your WiFi>"
    psk="<Password for your WiFi>"
    }

- Put waveshare SIM868 GSM hat on raspberry zero w. Both jumpers at B (in the middle). No other connections necessary. The gsm hat needs to be turned on separately with its power key.


- After startup ssh with pi and raspberrypi (user/pass)
    - sudo raspi-config
    - Interfacing Options
    - F6 Serial -> No -> Yes
    
- Then install minicom: sudo apt-get install minicom
- minicom -D /dev/ttyS0  (just to check, takes a while to react after opening it)
- send AT. If OK comes back, all is good. 


- sudo apt install python3-pip
- pip3 install python-gsmmodem-new