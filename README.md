# dynamicTelegramBot
dynamic telegram bot for domoticz written in Python 2.7

You can use it by installing telepot using: pip install telepot

To secure the bot there you must place usernames in the array unames on line 163:
unames = ['username1', 'username2'] 

by using this the bot will only react to the users which are in the array.

Using this bot you can ask him for an switch/scene/group/utility switch. 
After the bot found the device it will ask you what you want to do with it (on,off)

If the device is an selector switch the bot will build special keyboard in telegram where you can find you're selector options from domoticz. 

But sometimes you don't know the full name of the device or you forget an character, in that case the bot will look for devices that could be the device that you want and will come with suggestions. 

So for example if you have 2 switches called livingroomSpeaker, livingroomLights

If you type livingroomspeaker to the bot it will come with the switch and asks you what you want to do (on or off)

but if you type living the bot will make an suggestions and asks if you meant one of the following devices and comes with livingroomSpeaker and livingroomLights. 

Examples:
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/suggestions.png?raw=true)
