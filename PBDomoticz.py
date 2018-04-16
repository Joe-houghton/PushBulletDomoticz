#!/usr/bin/env python
__author__ = 'Joe Houghton'
import logging
import requests

from pushbullet import Listener
from pushbullet import Pushbullet


# CONFIG START

API_KEY = ''
HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None

DOMOTICZ_USER = ''
DOMOTICZ_PASS = ''
DOMOTICZ_ADDRESS = 'http://192.168.0.1:8080'

#CONFIG END

DomoticzDevice = namedtuple("DomoticzDevice", "name idx type")
devicesAndScenes = []
pb = None

def populateUsingURL(url, deviceType):
    requestUrl = DOMOTICZ_ADDRESS + url
    response = requests.get(requestUrl, auth=(DOMOTICZ_USER, DOMOTICZ_PASS))
    if response.status_code != 200:
        print("Bad Request")
        return None
    jsonDevices = response.json()
    devices = jsonDevices["result"]
    for device in devices:
        tempDevice = DomoticzDevice(device["Name"], device["idx"], deviceType)
        devicesAndScenes.append(tempDevice)

def populateDevicesAndScenes():
    devicesAndScenes = []
    getAllSwitches = "/json.htm?type=command&param=getlightswitches"
    populateUsingURL(getAllSwitches, 0)
    getAllScenes = "/json.htm?type=scenes"
    populateUsingURL(getAllScenes, 1)

def doesDeviceExist(deviceName):
    deviceNameToTest = deviceName.lower()
    for device in devicesAndScenes:
        if device[0].lower() == deviceNameToTest :
            return device
    return None

def getTargetDevice(words):
    print("finding device...")
    wordsLength = len(words)
    targetDevice = ""
    for i in range(wordsLength - 2):
        if i > 0 :
            targetDevice += " "
        targetDevice += words[i + 2]
        returnDevice = doesDeviceExist(targetDevice)
        if returnDevice != None :
            return returnDevice

    print("No matches for " + targetDevice)
    return None # No matches


def sendCommand(command, deviceId, deviceType):
    # e.g. '/json.htm?type=command&param=switchscene&idx=1'
    url = ""
    param = ""
    
    if deviceType == 0:
        param = "switchlight"
    elif deviceType == 1:
        param = "switchscene"

    jsonString = '/json.htm?type=command&'
    switchCommand = '&switchcmd='
    seq = (DOMOTICZ_ADDRESS, jsonString, "param=", param, "&idx=", deviceId, switchCommand, command)
    blankString = ''
    url = blankString.join(seq)

    print(url, '\n')
    response = requests.get(url, auth=(DOMOTICZ_USER, DOMOTICZ_PASS))
    if response.status_code != 200:
        print("Bad Send Request")
        return None


def getNewPushes():
    pushes = pb.get_pushes()
    populateDevicesAndScenes()
    for push in pushes:
        if not isinstance(push,dict): 
            # not a push object
            continue
        print(push.get('title', ''))
        message = push.get('body', '')
        print(message)
        lines = message.split('\n')
        deletePush = False
        for line in lines:
            words = line.split(' ')
            if len(words) > 2:
                if words[0] == '#command':
                    deletePush = True
                    sendCommand(words[1], words[2], 0)
                elif words[0] == '#commandToScene':
                    deletePush = True
                    sendCommand(words[1], words[2], 1)
                elif words[0] == '#commandByName':
                    print("Processing Command by Name")
                    deletePush = True
                    targetDevice = getTargetDevice(words)
                    if targetDevice != None:
                        print("Target Device is " + targetDevice[0])
                        sendCommand(words[1], targetDevice[1], targetDevice[2])
                    else:
                        print("Cannot find device: ")
        if deletePush:    
            pb.dismiss_push(push.get('iden'))
            pb.delete_push(push.get("iden"))
                

def on_push(data):
    print('Received data:\n{}'.format(data))
    if data['type'] == 'tickle':
        if data['subtype'] == 'push':
            getNewPushes()


def main():
    global pb
    print('got this far')
    pb = Pushbullet(API_KEY)
    print('got a pb instance')
    s = Listener(account=pb,
                 on_push=on_push,
                 http_proxy_host=HTTP_PROXY_HOST,
                 http_proxy_port=HTTP_PROXY_PORT)
    pb.delete_pushes() #lets delete any pushes  that we already have so they do not trigger now
    try:
        s.run_forever()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    main()
