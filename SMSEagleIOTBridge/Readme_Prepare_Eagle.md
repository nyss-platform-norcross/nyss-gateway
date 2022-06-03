# 1. Preparations before deployment

## 1.1. Enter the shell on the SMSEagle

1. Find the correct IP address for the SMSEagle
```
arp -a
```
There is a MAC Address on the bottom of the device to confirm the correct IP address.

2. Open a shell on the SMSEagle
```
ssh root@ipOfEagle
```

## 1.2. Enter SMSEagle web interface

1. Enter the IP Address of the Eagle in the browser

2. Log in with the standard admin credentials (admin/password)

3. Go to Settings -> Date/Time and change the time to UTC


## 1.3. Set up user for Azure IoT Hub connection

1. In the Eagle web interface, find 'users' in the left vertical navbar

2. Add a user at the far top right 

3. Use whatever name/password combination you want

4. The level should be user

5. Set the API access to custom with access to only 'send_sms'

## 1.4. Configure new SMSEagle in Azure

1. Go to Azure > IoT Hub > Device management > Devices

2. Press 'Add Device'

3. Fill in a Device ID (the rest of the settings can be standard)

4. Copy 'Primary Connection String' (you will need this later)

## 1.5. Install Python 3.6.5 and dependencies on SMSEagle

1. Make sure you are inside a bash on the SMSEagle, as described in 1.1.2

2. Run these commands

```
cd /home/pi

do-not-use_apt-get update

do-not-use_apt-get install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git

wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
```
3. Configure Python 3.6.5 

Ideally we want to run these commands with the --enable-optimizationsn flag, but this is very time consuming, and might fail. If so, simply run the command without it. 
```
./configure --enable-optimizations
make -j -l 4
make altinstall
```

4. Add a new alias to the bashrc:

Enter the text editor for bashrc with the following command:
```
nano ~/.bashrc
```
Add this alias to the bash

```
alias python3='python3.6'
```

5. Reboot the device

6. Check Phyton version

```
python3 -V
```

should give

```
Python 3.6.5
```

7. Upgrade pip and install dependencies

```
python3 -m pip install --upgrade pip
```

After that, pip3 should be usable to install the azure-iot-hub module:

```
pip3 install azure-iot-device
```

# 2 Deployment

### 2.1. Copy python script
The connection of the SMSEagle to the Azure IOT hub is done via a python script. That script runs on the SMSEagle. The Azure IOT hub connection string and the user for the http API of the SMSEagle need to be set.

The python script is developed in the following repository:
* https://github.com/nyss-platform-norcross/nyss-sms-gateway

1. Enter the correct folder

```
cd /home/pi
```

2. Download the following scripts with curl

```
curl -o nyssIoTBridge.py https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/master/SMSEagleIOTBridge/nyssIotBridge.py 

curl -o smsEagle-iot-hub-handler.py https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/master/SMSEagleIOTBridge/smsEagle-iot-hub-handler.py
```

### 2.2. Copy service files

1. Enter the correct folder

```
cd /etc/systemd/system
```
2. Download service files with curl
```
curl -o nyss-iot-bridge.service https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/master/SMSEagleIOTBridge/nyss-iot-bridge.service 

curl -o nyssIoTBridgeBoot.sh https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/master/SMSEagleIOTBridge/nyssIotBridgeBoot.sh
```
3. Set the access rights on the files
```
chmod 644 /etc/systemd/system/nyss-iot-bridge.service
chmod +x /home/pi/smsEagle-iot-hub-handler.py
```

### 2.4. Download and run setup script

This repository also contains a setup shell script that can be downloaded to skip steps 2.3-2.4

1. Download setup script

```
curl -o setup.sh https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/master/SMSEagleIOTBridge/setup.sh
```
2. Make it executable
```
chmod +x setup.sh
```
3. Run the script
```
bash setup.sh
```
The terminal will prompt you to add the environment variables necessary to run the service file. 
IOT_HUB_CONNECTIONSTRING = connection string from Azure IoT device
SMSEAGLE_USERNAME = username created in SMSEagle (Step 1.3.3)
SMSEAGLE_PWD = password created in SMSEagle (Step 1.3.3)



### 2.3. Set environment variables

(This step is only necessary if you did not run the setup script)

The python service on the SMSEagle tries to retrieve the IOT Hub connecting string and the login details for the SMSEagles http API either from arguments to starting the script or from environment variables (arguments take precedence). The environment variables should be set in the following way. This way makes it sure for the user that the SMSEagles services are run on, has access to the env variables.

1. Create correct folder path

```
mkdir /home/pi
```  


2. Check that the service file is in the correct place

After the service is configured as in the previous chapter, the following file should exist:

```
/etc/systemd/system/nyss-iot-bridge.service
```
The environment variables are configured using a so called Drop-In file.  The following describes how to create and fill it directly on the SMSEagle.

3. Create the following folder
```
mkdir /etc/systemd/system/nyss-iot-bridge.service.d
``` 
4. Create the file
``` 
touch /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
```

5. Enter text editor

```
nano /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
``` 

6. Fill in environment variables

The file takes the environment variables and should look e.g. as such (make sure that if you just copy it from here, and paste using nano, you are not missing the beginning of the first line. The buffer seems to be too small.):

```
[Service]
Environment="IOT_HUB_CONNECTIONSTRING=HostName=iothuburl;DeviceId=somedevice;SharedAccessKey=somerandomkey"
Environment="SMSEAGLE_USERNAME=usernameyoucreatedbefore"
Environment="SMSEAGLE_PWD=pwdyoucreatedbefore"
```
The connection string is what you configured in step 1.4.4
The username and password is what you configured in step 1.3.3

## 2.4 Start service & Wrap up

1. Reload and restart service file

```
systemctl daemon-reload
systemctl enable nyss-iot-bridge.service
systemctl start nyss-iot-bridge.service
reboot
```

3. You can also check the python script log
```
nano /var/log/iot-bridge-log.log
```

# 3. Status checks and common failures

## 3.1 Check the service is running
After reboot, run the following command
´´´
systemctl status nyss-iot-bridge.service
´´´
The message should show something like this
´´´
 nyss-iot-bridge.service - This is the service for the iot bridge to azure
   Loaded: loaded (/etc/systemd/system/nyss-iot-bridge.service; enabled)
  Drop-In: /etc/systemd/system/nyss-iot-bridge.service.d
           └─override.conf
   Active: active (running) since Mon 2020-03-09 10:48:17 GMT; 1h 56min ago
 Main PID: 1699 (python3)
   CGroup: /system.slice/nyss-iot-bridge.service
           └─1699 /usr/bin/python3 /home/pi/smsEagle-iot-hub-handler.py

Mar 09 10:48:17 smseagle systemd[1]: Started This is the service for the iot bridge to azure.
´´´
#  4. Post old SMS from the SMSEagle to the platform

## 4.1. Motivation

Sometimes the SMSEagle does not have a local internet connection, while the mobile network continues to work. In that situation, the Eagle will continue to receive SMS, but they will not be posted to the platform after 24 hours of their arrival in the SMSEagle.

This document describes how to make the Eagle repost them to the Nyss platform.

## 4.2. Preparation

1) Turn off the 24 hours limit (perhaps this step can be skipped, if we copy a date less than 24 hours in the past into the callback queue table!)

SSH into the Eagle. Go to the file /mnt/ramdisk/www/application/plugins/callback/models/callback_model.php .
Find the "function process_waiting_queque()".

In that function find the following lines and comment them out using // .
```
$limit_date = date("Y-m-d H:i:s", strtotime('-24 hours'));
$this->db->where('sms_timestamp <', $limit_date);
$this->db->delete('plugin_callback_waitqueue');
``` 
If you want to make that stick after a reboot, you'll have to do the same in the file /var/www/application/plugins/callback/models/callback_model.php .

1) Make the Eagle send Received timestamp instead of Update in DB

In its default configuration, the Eagle posts the UpdatedInDB timestamp to the platform. Since we want to see the ReceivingDateTime stamp in the platform, we'll need to change this (usually there is no huge difference, since its immediately posted, so its not a big issue).

In the file /mnt/ramdisk/www/application/plugins/callback/models/callback_model.php find the function "function process_waiting_queque()".

Find the following line:
```
$this->db->select('ID, SenderNumber, UpdatedInDB, TextDecoded, id_rule, oid, RecipientID, id_waitqueue');
```
and rewrite it to
```
$this->db->select('ID, SenderNumber, ReceivingDateTime, TextDecoded, id_rule, oid, RecipientID, id_waitqueue');
```
i.e. change UpdatedInDB to ReceivingDateTime.

In addition find the following line:
``` 
$ts = strtotime($row->UpdatedInDB);
``` 
and rewrite it to
``` 
$ts = strtotime($row->ReceivingDateTime);
``` 
i.e. change UpdateInDB to ReceivingDateTime.

If you want to make that stick after a reboot, you'll have to do the same in the file /var/www/application/plugins/callback/models/callback_model.php .


## 4.3. Making the SMSEagle repost the SMS

The Eagle uses a postgresql database. SMS are stored in the inbox table. The callback plugin uses a queue table in the same database. That table is regularly (every couple of minutes) checked, and every entry in there is posted to whatever is defined as a callback rule.
Hence we can just copy over all the SMS we want to repost from the inbox table to the callback table.

1) If you are not connected to the Eagle via SSH, do it now :).
2) If you don't want to do adjust the callback deletion time from 24 hours to infinite, you can trick the callback into thinking the messages are more recent, by adding a current time/date into the plugin_callback_waiting_queue with a statement such as this:
````
psql -U postgres -d smseagle -c "INSERT INTO plugin_callback_waitqueue (id_inbox, sms_timestamp) SELECT \"ID\", '2020-02-20 05:00:00' FROM inbox WHERE \"ReceivingDateTime\" >= '2018-01-01 00:00:00' and \"ReceivingDateTime\" < '2020-02-19 00:00:00';"
````
You'd have to replace "2020-02-20 05:00:00" with something in the last 24 hours and "2018-01-01 00:00:00" with the beginning of the timerange you want to repost and "2020-02-19 00:00:00" with the end of the time range you want to post.

3) If you want to repost reports from a specific time range, use a psql statement such as the following:
````
psql -U postgres -d smseagle -c "INSERT INTO plugin_callback_waitqueue (id_inbox, sms_timestamp) SELECT \"ID\", \"ReceivingDateTime\" FROM inbox WHERE \"ReceivingDat
eTime\" >= '2018-01-01 00:00:00' and \"ReceivingDateTime\" < '2020-02-19 00:00:00';"
````
4) If you want to repost reports from a specific number/Data Collector, use a psql statement such as the following:
````
psql -U postgres -d smseagle -c "INSERT INTO plugin_callback_waitqueue (id_inbox, sms_timestamp) SELECT \"ID\", \"ReceivingDateTime\" FROM inbox WHERE \"SenderNumber\" = 'sendernumber in format ++479999999';"
````
5) If you have not also edited the file /var/www/application/plugins/callback/models/callback_model.php, everything will default back to the SMSEagles original php code after you reboot.
