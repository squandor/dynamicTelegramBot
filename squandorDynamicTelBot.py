## Created by Squandor v0.1
import os
import sys
import time
import random
import datetime
import telepot
import urllib
import urllib2
import json
import re
import base64
from random import randint
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from collections import Counter

########### Config ###############
url = 'http://<domoticz_ip>:8080'
bot_token = '<botToken>'
unames = ['', ''] ## usernames which can use the bot in telegram
car_location_idx = '111' #lat,long
##################################
def getRandom():
   return randint(0, 9)

def getDomoticzUrl(url):
    try:
        _res = json.load(urllib2.urlopen(url))
    except:
        _res = ''
    return _res

def getSelectorNames(_idx):
    _levelActions = base64.b64decode(getDomoticzUrl(url + '/json.htm?type=devices&rid=' + _idx)['result'][0]['LevelNames']).split('|')
    _lvls = 0
    _levels = []
    for _level in _levelActions:
        _obj = {}
        _obj['Name'] = _level
        if _lvls != 0:
            _obj['level'] = str(_lvls) + '0'
        else:
            _obj['level'] = '0'
        _lvls += 1
        _levels.append(_obj)
    return _levels

def getIDXByName(name, _devices):
    _idx = {'idx': '', 'suggestions': [], 'type': '', 'levels': []}
    for i in _devices:
        if i['Name'].lower() == name.lower():
            _idx['idx'] = i['idx']
            if 'SubType' in i:
                _idx['type'] = i['SubType'].replace(' ', '_')
            else:
                _idx['type'] = i['Type'].replace(' ', '_')
            if _idx['type'].lower() == 'selector_switch':
                _idx['levels'] = getSelectorNames(i['idx'])
            break
        if re.search('.*' + name.lower() + '.*', i['Name'].lower().strip()):
            _sugObject = {}
            _sugObject['idx'] = i['idx']
            if 'SubType' in i:
                _sugObject['type'] = i['SubType'].replace(' ', '_')
            else:
                _sugObject['type'] = i['Type'].replace(' ', '_')
            _sugObject['Name'] = i['Name']
            if _sugObject['type'].lower() == 'selector_switch':
                _sugObject['levels'] = getSelectorNames(i['idx'])
            _idx['suggestions'].append(_sugObject)
    return _idx

def getNameByIDX(dev, _devices):
    for i in _devices:
        if i['idx'] == dev['idx']:
            _type = ''
            if 'SubType' in i:
                _type = i['SubType'].replace(' ', '_')
            else:
                _type = i['Type'].replace(' ', '_')
            if _type.lower() == dev['type'].lower():
                _status = ''
                if _type.lower() == 'selector_switch':
                    _stateCount = i['Status'].replace('Set Level: ', '').replace(' %', '')
                    for i in getSelectorNames(i['idx']):
                        if i['level'] == _stateCount:
                            _status = i['Name'].title()
                else:
                    try:
                        _status = i['Status'].title()
                    except:
                        _status = i['Data']

                return i['Name'].title(), _status

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    if query_data.lower().split(' ')[0] == '/switch':
        bot_text = ''
        runUrl = url + '/json.htm?type=command&param=switchlight&idx=' + query_data.lower().split(' ')[1] + '&switchcmd=' + query_data.lower().split(' ')[2].title().replace('Level=', 'level=').strip()
        _res = getDomoticzUrl(runUrl)
        if _res['status'].lower() == 'ok':
            bot_text = 'Commando uitgevoert'
        else:
            bot_text = 'Er ging iets mis met het uitvoeren: ' + runUrl
        bot.answerCallbackQuery(query_id, text=bot_text)
    elif query_data.lower().split(' ')[0] == '/group':
        bot_text = ''
        runUrl = url + '/json.htm?type=command&param=switchscene&idx=' + query_data.lower().split(' ')[1] + '&switchcmd=' + query_data.lower().split(' ')[2].title().replace('Level=', 'level=').strip()
        _res = getDomoticzUrl(runUrl)
        if _res['status'].lower() == 'ok':
            bot_text = 'Commando uitgevoert'
        else:
            bot_text = 'Er ging iets mis met het uitvoeren: ' + runUrl
        bot.answerCallbackQuery(query_id, text=bot_text)
    elif query_data.lower().split(' ')[0] == '/utility':
        bot_text = ''
        runUrl = url + '/json.htm?type=devices&rid=' + query_data.lower().split(' ')[1]
        _res = getDomoticzUrl(runUrl)
        if _res['status'].lower() == 'ok':
            bot_text = 'Commando uitgevoert'
        else:
            bot_text = 'Er ging iets mis met het uitvoeren: ' + runUrl

        bot.answerCallbackQuery(msg['chat']['id'], text=_res['result']['Data'])
    elif query_data.lower().split(' ')[0] == '/suggestion':
        _utility = getDomoticzUrl(url + '/json.htm?type=devices&filter=utility&used=true')['result']
        _utilityTypes = sorted(Counter(x['SubType'].lower() for x in _utility if 'SubType' in x)) + sorted(Counter(x['Type'].lower() for x in _utility if 'Type' in x))
        if query_data.lower().split(' ')[2] == 'switch':
            _callbackCommand = '/switch ' + query_data.lower().split(' ')[1]+ ' '
            markup_dyn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='On', callback_data=_callbackCommand + 'on'), InlineKeyboardButton(text='Off', callback_data=_callbackCommand + 'off')],
            ])
        elif query_data.lower().split(' ')[2] == 'group':
            _callbackCommand = '/group ' + query_data.lower().split(' ')[1]+ ' '
            markup_dyn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='On', callback_data=_callbackCommand + 'on'), InlineKeyboardButton(text='Off', callback_data=_callbackCommand + 'off')],
            ])
        elif query_data.lower().split(' ')[2] in _utilityTypes:
            _callbackCommand = '/utility ' + query_data.lower().split(' ')[1]+ ' '
            markup_dyn = None
        elif query_data.lower().split(' ')[2] == 'selector_switch':
            _arr = []
            _callbackCommand = '/switch ' + query_data.lower().split(' ')[1] + ' '
            for i in getSelectorNames(query_data.lower().split(' ')[1]):
                _arr.append(
                InlineKeyboardButton(text=i['Name'], callback_data=_callbackCommand + 'Set%20Level&level=' + i['level'])
                )

            markup_dyn = InlineKeyboardMarkup(inline_keyboard=[_arr])
        _name, _state = getNameByIDX({'idx': query_data.lower().split(' ')[1], 'type': query_data.lower().split(' ')[2]}, getDomoticzUrl(url + '/json.htm?type=devices&filter=light&used=true')['result'] + getDomoticzUrl(url + '/json.htm?type=scenes')['result'] + getDomoticzUrl(url + '/json.htm?type=devices&filter=utility&used=true')['result'])
        bot.sendMessage(int(query_data.split(' ')[3]), 'The ' + query_data.lower().split(' ')[2].title() + ' ' + _name + ' is currently  ' + _state + '. What do you want to do?', reply_markup=markup_dyn)


def handle(msg):
   chat_id = msg['chat']['id']
   command = msg['text']
   user = msg['from']['username']
   markup_main = ReplyKeyboardMarkup(keyboard=[['Car']],one_time_keyboard=False)
   markup_car = ReplyKeyboardMarkup(keyboard=[['Get location'], ['Back']], one_time_keyboard=False)
   run = False
   if user.lower() in unames:
       if command.lower() != '/start':
           command = command.lower().replace('/', '')
       if command.lower() == '/start':
           bot.sendMessage(chat_id, 'What can I do for you?', reply_markup=markup_main)
       if command.lower() == 'back':
           bot.sendMessage(chat_id, 'What can I do for you?', reply_markup=markup_main)
       if command.lower() == 'car':
           bot.sendMessage(chat_id, 'What do you want to know?', reply_markup=markup_car)
       elif command.lower() == 'get location':
           url += '/json.htm?type=devices&rid=' + car_location_idx
           _f = urllib2.urlopen(url)
           _jsonObj = json.load(_f)
           _mapurl = 'https://www.google.com/maps/search/?api=1&query=' +  _jsonObj['result'][0]['Data']
           bot.sendMessage(chat_id, _mapurl)
       else:
           if command.lower() != '':
               _switches = getDomoticzUrl(url + '/json.htm?type=command&param=getlightswitches')['result']
               _groups = getDomoticzUrl(url + '/json.htm?type=scenes')['result']

               _utility = getDomoticzUrl(url + '/json.htm?type=devices&filter=utility&used=true')['result']
               _utilityTypes = sorted(Counter(x['SubType'].lower() for x in _utility if 'SubType' in x)) + sorted(Counter(x['Type'].lower() for x in _utility if 'Type' in x))
               _devices = _switches + _groups + _utility
               _idx = getIDXByName(command.lower(), _devices)
               if _idx['idx'] != '':
                   if _idx['type'].lower() == 'switch' or _idx['type'].lower() == 'x10':
                       _callbackCommand = '/switch ' + _idx['idx'] + ' '
                       markup_dyn = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='On', callback_data=_callbackCommand + 'on'), InlineKeyboardButton(text='Off', callback_data=_callbackCommand + 'off')],
                       ])
                   if _idx['type'].lower() == 'scene' or _idx['type'].lower() == 'group':
                       _callbackCommand = '/group ' + _idx['idx'] + ' '
                       markup_dyn = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='On', callback_data=_callbackCommand + 'on'), InlineKeyboardButton(text='Off', callback_data=_callbackCommand + 'off')],
                       ])
                   elif _idx['type'].lower() == 'selector_switch':
                       _arr = []
                       _callbackCommand = '/switch ' + _idx['idx'] + ' '
                       for i in _idx['levels']:
                           _arr.append(
                           InlineKeyboardButton(text=i['Name'], callback_data=_callbackCommand + 'Set%20Level&level=' + i['level'])
                           )
                       markup_dyn = InlineKeyboardMarkup(inline_keyboard=[_arr])
                   elif _idx['type'].lower() in _utilityTypes:
                       _callbackCommand = '/utility ' + _idx['idx'] + ' '
                       markup_dyn = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='Show status', callback_data=_callbackCommand + 'status')],
                       ])
                   bot.sendMessage(chat_id, 'What do you want to do with the switch ' + str(chat_id) + ' ' + command.lower() + '?', reply_markup=markup_dyn)
               else:
                   if len(_idx['suggestions']) > 0:
                       _arr = []
                       for i in _idx['suggestions']:
                           _arr.append(InlineKeyboardButton(text=i['Name'], callback_data='/suggestion ' + i['idx'] + ' ' + i['type'] + ' ' + str(chat_id)))

                       markup_dyn = InlineKeyboardMarkup(inline_keyboard=[_arr])
                       bot.sendMessage(chat_id, 'Kon het apparaat niet vinden bedoelde je soms een van de onderstaande?', reply_markup=markup_dyn)
                   else:
                       bot.sendMessage(chat_id, 'Kon het apparaat niet vinden')
       if run:
           getDomoticzUrl(url)

## huisserver
bot = telepot.Bot(bot_token)
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print 'I am listening...'

while 1:
    time.sleep(10)
