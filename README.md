# dynamicTelegramBot
dynamic telegram bot for domoticz written in Python 2.7
You can use it by installing telepot and ConfigParser using: pip install telepot ConfigParser

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

# First run
On the first run it will ask you some information:
- url: <domoticz_url> (http://192.168.1.2:8080)
- bot_token
- unames (usernames seperated by an comma): user1, user2, user3
- car_location_idx: can be an idx number of an text utility which as the lat,long in it.
after that an config.ini will be created and it will run.

# Systemd script
Thanks to so help someone made an easy service file so you can easy run the bot using the systemd service. 
The example is in the repo. 
You can use it using the following steps
Copy code to /etc/systemd/system/messagebot.service
Edit the values in the example script:

[Unit]<br>
Description=Telegram Bot for Domoticz After=multi-user.target<br>
[Service]<br>
Type=idle<br>
User=<username><br>
ExecStart=/usr/bin/python /home/<username>/scripts/telegram/dynamicTelegramBot/squandorDynamicTelBot.py<br>
WorkingDirectory=/home/<username>/scripts/telegram/dynamicTelegramBot/<br>
[Install]<br>
WantedBy=multi-user.target<br>
<br>
"sudo chmod 655 /etc/systemd/system/messagebot.service"<br>
"sudo systemctl daemon-reload"<br>
"sudo systemctl enable messagebot.service"<br>
"sudo systemctl start messagebot.service"<br>
"sudo systemctl status messagebot.service"<br>

# Examples:<br>
Switch<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/example_switch.png?raw=true)

Selector Switch<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/selector_switch.png?raw=true)

Suggestions<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/suggestions.png?raw=true)

Car Location<br>
![alt text](https://github.com/squandor/dynamicTelegramBot/blob/master/examples/car_getLocation.png?raw=true)
