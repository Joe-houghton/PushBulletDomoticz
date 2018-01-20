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

pb = None

def sendCommand(command, device):
    jsonString = '/json.htm?type=command&param=switchlight&idx='
    switchCommand = '&switchcmd='
    seq = (DOMOTICZ_ADDRESS, jsonString, device, switchCommand, command)
    blankString = ''
    url = blankString.join(seq)
    print(url, '\n')
    requests.get(url, auth=(DOMOTICZ_USER, DOMOTICZ_PASS))


def getNewPushes():
    pushes = pb.get_pushes()
    for push in pushes:
        if not isinstance(push,dict): 
            # not a push object
            continue
        print(push.get('title', ''))
        message = push.get('body', '')
        print(message)
        words = message.split(' ')
        if len(words) > 2:
            if words[0] == '#command':
                pb.dismiss_push(push.get('iden'))
                pb.delete_push(push.get("iden"))
                sendCommand(words[1], words[2])
                

def on_push(data):
    print('Received data:\n{}'.format(data))
    if data['type'] == 'tickle':
        if data['subtype'] == 'push':
            print('mhuwaaaaa\n')
            getNewPushes()


def main():
    global pb
    pb = Pushbullet(API_KEY)

    s = Listener(account=pb,
                 on_push=on_push,
                 http_proxy_host=HTTP_PROXY_HOST,
                 http_proxy_port=HTTP_PROXY_PORT)
    try:
        s.run_forever()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    main()
