# PushBulletDomoticz
Using PushBullet to push notifications to trigger Domoticz switches.

This can be used with Ifttt to trigger from Google Assistant. I found this to be the best method to not having to expose your Pi to the Internet by opening router ports. The other benefit is that people can not view your password in plain text (when not using https, which is a pain to set up and renew).

## Installation
The following instructions are based on installation for the Raspberry Pi:

If you require Python:
```
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.7
```

Other Dependencies:
```
sudo apt-get install python-pip git
```
Now pip is installed, lets install the fantastic Pushbullet.py library, (using pip installs all the required libraries automatically):
```
sudo pip install pushbullet.py
```
Now lets copy this project, ready for configuring:
```
cd ~/
mkdir scripts
cd scripts
git clone https://github.com/Joe-houghton/PushBulletDomoticz.git
cd PushBulletDomoticz
```
## Configuration
Goto https://www.pushbullet.com/ and create an account, if you already have an account, I suggest creating a new one, to not get notified every time you want to turn the lights on

Now go to https://www.pushbullet.com/#settings and click **Create Access Token**. Save this token, you will need it later.

Lets configure the settings by editing:
```
nano ~/scripts/PushBulletDomoticz/PBDomoticz.py
```

Fill out the config section with your details (between **#CONFIG START** and **#CONFIG END**
Paste your access token from the pushbullet website in the **API_KEY**
Fill out your Domoticz Username and password and the IP or address (includingthe port) e.g. 192.168.0.1:8080

## Push format
The format is as follows:
```
#command On Idx
```
So to turn on a switch that has an id of 14, we would send:
```
#command On 14
```
And to turn it off
```
#command Off 14
```
Other commands available are:
```
#commandToScene On 2
#commandByName Off Main Light
#commandByName On Evening Lighting
```
Note: The #commandByName matches the text with your device and scene names.
To find the Idx go to your Domoticz Url and click on Setup > Devices. This will give you a table of devices that you have set up along with their Idx's. 

## Use with Ifttt
Create an applet with an 'If' of Google assistant, Alexa, or whatever you like.
Set up the 'That' to be pushbullet (make sure that you connect with the same credentials that you got your Auth token with).
Using the format mentioned above, push a note with the title e.g. 'Turn on Lamp' and the message as '#command On 14'

## Test that everything works
Run the following command and then send a push e.g. #command On 14
```
python /home/pi/scripts/PushBulletDomoticz/PBDomoticz.py
```

## Adding to startup
First lets create the logs directory.
There are actually many ways to add to startup, the simplest I have found is to add to /etc/rc.local
```
mkdir /home/pi/logs
sudo nano /etc/rc.local
```
Add the following to the bottom (before exit 0)
```
python /home/pi/scripts/PushBulletDomoticz/PBDomoticz.py  > /home/pi/logs/pushbullet.log 2>&1
```

reboot - test - done!
