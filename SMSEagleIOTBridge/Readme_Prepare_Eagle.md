# 1. Preparations before deployment
## 1.2. Setup of Azure IOT-Hub connection 
### 1.2.1. Create user for python script
* Find the IP of your SMSEagle
* Login with details admin/password
* Click users in the left vertical navbar
* Add a user at the far top right
* Use whatever name and password combination you want, but it needs to match whatever you set in the environment variables in 1.2.5
* The level should be user
* Access to API MUST should be turned to custom and access to send_sms
* If the custom access is to difficult you can also set it to on :)
### 1.2.2. Install python3 and dependencies on SMSEagle

You only have to do 1.2.2.1 or 1.2.2.2. If you have managed to install it with 1.2.2.1 you can jump directly to 1.2.3.!

#### 1.2.2.1. The easy way :)

The following commands have to be run from a shell on the SMSEagle. So first find the IP of the SMSEagle and then use:
```
ssh root@IPofEagle
```

and then install Python3 from there.

* do-not-use_apt-get update
* do-not-use_apt-get install python3
* do-not-use_apt-get install python3-pip
* pip3 install azure-iot-device

Sometimes the above method does not work. E.g. when you want to use pip3 to install the module, you get an error saying the requests module is not installed. Or if you want to upgrade pip using python3, you get an error asking for a python version above 3.5. In this case use the second way.

#### 1.2.2.2. The hard way :(

If you have to do it in the way described below, you will have to edit the service file to account for the different python path! Its described in Ch 1.2.4. For reference, change as follows:

```
ExecStart=/usr/bin/python3 /home/pi/smsEagle-iot-hub-handler.py
```

to 

```
ExecStart=/usr/local/bin/python3.6 /home/pi/smsEagle-iot-hub-handler.py
```

Apart from that, u can use the following commands to install python version 3.6.5.

```
cd /home/pi

do-not-use_apt-get update

do-not-use_apt-get install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git

wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure --enable-optimizations
make -j -l 4
make altinstall

vi ~/.bashrc
```
Add a new alias to the bashrc:

```
alias python3='python3.6'
```

Reboot.

```
python3 -V
```

should give

```
Python 3.6.5
```

Then you can upgrade pip

```
python3 -m pip install --upgrade pip
```

After that pip3 should be usable to install the azure-iot-hub module:

```
pip3 install azure-iot-device
```

### 1.2.3. Copy python script
The connection of the SMSEagle to the Azure IOT hub is done via a python script. That script runs on the SMSEagle. The Azure IOT hub connection string and the user for the http API of the SMSEagle need to be set.

The python script is developed in the following repository:
* https://github.com/nyss-platform-norcross/nyss-sms-gateway

You need the following files:
* https://github.com/nyss-platform-norcross/nyss-sms-gateway/blob/sms-eagle-iot-connection/SMSEagleIOTBridge/nyssIotBridge.py 
* https://github.com/nyss-platform-norcross/nyss-sms-gateway/blob/sms-eagle-iot-connection/SMSEagleIOTBridge/smsEagle-iot-hub-handler.py

If the repository does not exist anymore for some reason, you can probably find the files on one of the existing SMSEagles in the folder /home/pi. 
After you have downloaded them, make sure that the filename is exactly that, and e.g. windows did not "accidentally" add .txt as an extension.

Copy the following files to the SMSEagles /home/pi folder:
```
nyssIotBridge.py
smsEagle-iot-hub-handler.py
```

Via ssh you can use the following commands:
```
scp "C:/path on windows to file" root@ipOfEagle:/home/pi
```

### 1.2.4. Copy service file

If you installed Python using what is described in Chapter 1.2.2.1., you can skip step 2.

#### 1. Get the necessary files

The service file is in the same repository as the python script:
- https://github.com/nyss-platform-norcross/nyss-sms-gateway

You need the following file:
* https://github.com/nyss-platform-norcross/nyss-sms-gateway/blob/sms-eagle-iot-connection/SMSEagleIOTBridge/nyss-iot-bridge.service

If the repository does not exist anymore for some reason, you can probably find the files on one of the existing SMSEagles in the folder /etc/systemd/system.

#### 2. Adjust path if necessary (only if you installed Python the hard way)
The path in that file needs to match whereever you have copied the smsEagle-iot-hub-handler.py file (usually that would be /home/pi).

If you had to install Python the hard way **(and only then)**, you need to change the path in the service to reach your python installation. Change the following:

```
ExecStart=/usr/bin/python3 /home/pi/smsEagle-iot-hub-handler.py
```

to 

```
ExecStart=/usr/local/bin/python3.6 /home/pi/smsEagle-iot-hub-handler.py
```

You might have to adjust that path, depending on where your installation is located. You can find that out using the following command:

```
whereis python3
```

#### 3. Copy the files

Copy the following file to the SMSEagles /etc/systemd/system folder:
```
nyss-iot-bridge.service
```

Via ssh you can use the following commands as run from your host computer and not the SMSEagle:
```
scp "C:/path on windows to file" root@ipOfEagle:/etc/systemd/system
```

SSH back to the SMSEagle and set the access rights on the files using the following commands:
```
ssh root@IPofEagle
chmod 644 /etc/systemd/system/nyss-iot-bridge.service
chmod +x /home/pi/smsEagle-iot-hub-handler.py
```

Continue by setting the necessary environment variables in the following chapter.

### 1.2.5. Set environment variables
The python service on the SMSEagle tries to retrieve the IOT Hub connecting string and the login details for the SMSEagles http API either from arguments to starting the script or from environment variables (arguments take precedence). The environment variables should be set in the following way. This way makes it sure for the user that the SMSEagles services are run on, has access to the env variables.

After the service is configured as in the previous chapter, the following file should exist:
```
/etc/systemd/system/nyss-iot-bridge.service
```
The environment variables are configured using a so called Drop-In file. Create the following folder. The following describes how to create and fill it directly on the SMSEagle. You can also create it on your host computer and copy it over using the scp commands described earlier.

As for the method to create it directly on the SMSEagle:
```
mkdir /etc/systemd/system/nyss-iot-bridge.service.d
```
and a file 
```
touch /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
```
The file takes the environment variables and should look e.g. as such (make sure that if you just copy it from here, and paste using vi, you are not missing the beginning of the first line. The buffer seems to be too small.):
```
[Service]
Environment="IOT_HUB_CONNECTIONSTRING=HostName=iothuburl;DeviceId=somedevice;SharedAccessKey=somerandomkey"
Environment="SMSEAGLE_USERNAME=usernameyoucreatedbefore"
Environment="SMSEAGLE_PWD=pwdyoucreatedbefore"
```

You can get the IOT_HUB_CONNECTIONSTRING variable from the Azure IOT Hub (Primary Connection String). The creation of the Eagle in Azure IOT Hub is described in the respective Readme file coming with the Nyss codebase. If that is not available, refer to the Microsoft tutorials on how to create an IOT device. 
The IOT_HUB_CONNECTIONSTRING is what is refered to as the Primary Connection String in Azure IOT Hub.

### 1.2.6. Start service & Wrap up

After configuring the above, you should run the following commands:

```
systemctl daemon-reload
systemctl enable nyss-iot-bridge.service
systemctl start nyss-iot-bridge.service
reboot
```

You can check the status of the service using:
```
systemctl status nyss-iot-bridge.service
```

The python scripts logs to:

```
/var/log/iot-bridge-log.log
```

You can check that log file using e.g.
```
vi /var/log/iot-bridge-log.log
```

Shift + G brings you to the bottom of the file in vim.

### 1.2.7. Check its working and common failures

After reboot the following command should:
```
systemctl status nyss-iot-bridge.service
```
should show something like the following:
```
 nyss-iot-bridge.service - This is the service for the iot bridge to azure
   Loaded: loaded (/etc/systemd/system/nyss-iot-bridge.service; enabled)
  Drop-In: /etc/systemd/system/nyss-iot-bridge.service.d
           └─override.conf
   Active: active (running) since Mon 2020-03-09 10:48:17 GMT; 1h 56min ago
 Main PID: 1699 (python3)
   CGroup: /system.slice/nyss-iot-bridge.service
           └─1699 /usr/bin/python3 /home/pi/smsEagle-iot-hub-handler.py

Mar 09 10:48:17 smseagle systemd[1]: Started This is the service for the iot bridge to azure.
```

A common failure would be if the environment variables are not set, or could not be found by the service.


If you had to install Python the hard way (as in Chapter 1.2.2.2.), then you might get the error below.

```
● nyss-iot-bridge.service - This is the service for the iot bridge to azure
   Loaded: loaded (/etc/systemd/system/nyss-iot-bridge.service; enabled)
  Drop-In: /etc/systemd/system/nyss-iot-bridge.service.d
           └─override.conf
   Active: failed (Result: exit-code) since Thu 2020-03-19 09:47:16 GMT; 4min 56s ago
  Process: 1223 ExecStart=/usr/bin/python3 /home/pi/smsEagle-iot-hub-handler.py (code=exited, status=1/FAILURE)
 Main PID: 1223 (code=exited, status=1/FAILURE)

Mar 19 09:47:15 smseagle-dev systemd[1]: Starting This is the service for the iot bridge to azure...
Mar 19 09:47:15 smseagle-dev systemd[1]: Started This is the service for the iot bridge to azure.
Mar 19 09:47:16 smseagle-dev python3[1223]: Traceback (most recent call last):
Mar 19 09:47:16 smseagle-dev python3[1223]: File "/home/pi/smsEagle-iot-hub-handler.py", line 1, in <module>
Mar 19 09:47:16 smseagle-dev python3[1223]: import nyssIotBridge
Mar 19 09:47:16 smseagle-dev python3[1223]: File "/home/pi/nyssIotBridge.py", line 4, in <module>
Mar 19 09:47:16 smseagle-dev python3[1223]: from azure.iot.device import IoTHubDeviceClient, MethodResponse
Mar 19 09:47:16 smseagle-dev python3[1223]: ImportError: No module named 'azure'
Mar 19 09:47:16 smseagle-dev systemd[1]: nyss-iot-bridge.service: main process exited, code=exited, status=1/FAILURE
Mar 19 09:47:16 smseagle-dev systemd[1]: Unit nyss-iot-bridge.service entered failed state.
```

That means you might have forgotten to adjust the service file as described at the beginning of chapter

#  2. Post old SMS from the SMSEagle to the platform

## 2.1. Motivation

Sometimes the SMSEagle does not have a local internet connection, while the mobile network continues to work. In that situation, the Eagle will continue to receive SMS, but they will not be posted to the platform after 24 hours of their arrival in the SMSEagle.

This document describes how to make the Eagle repost them to the Nyss platform.

## 2.2. Preparation

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


## 2.3. Making the SMSEagle repost the SMS

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