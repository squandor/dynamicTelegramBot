# dynamicTelegramBot
dynamic telegram bot for domoticz written in Python 2.7
You can use it by installing telepot using: pip install telepot

To secure the bot you must place usernames in the array unames:
unames = ['username1', 'username2'] 
by using this the bot will only react to the users which are in the array.

# What can it do?
Using this bot you can ask him for an switch/scene/group/utility switch. 
After the bot found the device it will ask you what you want to do with it (on,off)

If the device is an selector switch the bot will build special keyboard in telegram where you can find you're selector options from domoticz. 

But sometimes you don't know the full name of the device or you forget an character, in that case the bot will look for devices that could be the device that you want and will come with suggestions. 

So for example if you have 2 switches called livingroomSpeaker, livingroomLights

If you type livingroomspeaker to the bot it will come with the switch and asks you what you want to do (on or off)

but if you type living the bot will make an suggestions and asks if you meant one of the following devices and comes with livingroomSpeaker and livingroomLights. 

# Systemd script
Thanks to so help someone made an easy service file so you can easy run the bot using the systemd service. 
The example is in the repo. 
You can use it using the following steps
Copy code to /etc/systemd/system/messagebot.service
Edit the values in the example script:

[Unit]
Description=Telegram Bot for Domoticz After=multi-user.target
[Service]
Type=idle
User=<username>
ExecStart=/usr/bin/python /home/<username>/scripts/telegram/dynamicTelegramBot/squandorDynamicTelBot.py
[Install]
WantedBy=multi-user.target

"sudo chmod 655 /etc/systemd/system/messagebot.service"
"sudo systemctl daemon-reload"
"sudo systemctl enable messagebot.service"
"sudo systemctl start messagebot.service"
"sudo systemctl status messagebot.service"

# Examples:<br>
Switch<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/example_switch.png?raw=true)

Selector Switch<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/selector_switch.png?raw=true)

Suggestions<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/suggestions.png?raw=true)

Car Location<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/car_getLocation.png?raw=true)
