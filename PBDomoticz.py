#!/usr/bin/env python
__author__ = 'Joe Houghton'
import logging
import json
import requests

from pushbullet import Listener
from pushbullet import Pushbullet
from domoticz import Domoticz

# CONFIG START

API_KEY = ''
HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None

DOMOTICZ_USER = ''
DOMOTICZ_PASS = ''
DOMOTICZ_ADDRESS = 'http://192.168.0.1:8080'

#CONFIG END

domoticz = None
pb = None

def getNewPushes():
    pushes = pb.get_pushes()
    domoticz.populateDevicesAndScenes()
    for push in pushes:
        if not isinstance(push,dict): 
            # not a push object
            continue
        print(push.get('title', ''))
        message = push.get('body', '')
        print(message)
        deletePush = domoticz.ProcessCommand(message)
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
    print('Initialising')
    pb = Pushbullet(API_KEY)
    print('PB instance Created')
    s = Listener(account=pb,
                 on_push=on_push,
                 http_proxy_host=HTTP_PROXY_HOST,
                 http_proxy_port=HTTP_PROXY_PORT)
    print('Listening for pushes')
    
    
    domoticz = new Domoticz(DOMOTICZ_ADDRESS, DOMOTICZ_USER, DOMOTICZ_PATH)
    if domoticz == None:
        print('Cannot Initialise Domoticz, Check Configuration')
        exit()
    
    pb.delete_pushes() #lets delete any pushes  that we already have so they do not trigger now
    try:
        s.run_forever()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    main()
