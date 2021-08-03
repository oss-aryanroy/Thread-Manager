# About Thread-Manager

Default Prefix: `?`

Thread Manager is a Discord Bot written in python which uses discord.py 2.0.0a. It is used for logging thread activities within a discord server. in addition to logging, it also informs the staff of the server if a bad word/profane language is found in the name of the thread, however doesn't directly moderate it due to obvious reasons. It's also fully customizable, a specific role can be set to be pinged if slurs are found within thread name. Users can also set the channel they want the logs to be directed to. 


This bot was written with `python 3.8.5`, A higher version of python shouldn't pose a problem normally. If you do face an issue however, feel free to DM me on discord! `Pizerite#5648`

# Commands List [5]

  <ul>
  <li>?bind <#channel> - Setting logging channel</li>
  <li>?setprefix` <prefix> - Setting prefix of the bot</li>
  <li>?emergencyrole <@role> - Setting emergency role to be pinged (can be set to None)</li>
  <li>?invite - Invite for the bot (is generated automatically)</li>
  <li>?help - help for bot</li>
  </ul>
## Requiremenets

Thread Manager runs on python (if you couldn't tell) and it uses the following pip packages

```
aiosqlite profanity discord.py
```

To install aiosqlite:
      simply go to your cmd prompt or your virtual environment and type `python3 -m pip install aiosqlite` or `pip install aiosqlite`

To install profanity:

      simply go to your cmd prompt or your virtual environment and type python3 -m pip install profanity or pip install profanity

To install discord.py: (Note, thread manager uses discord.py 2.0.0 which is currently in alpha)

      simply go to your cmd prompt or your virtual environment and type python3 -m pip install -U git+https://github.com/Rapptz/discord.py or pip install git+https://github.com/Rapptz/discord.py
      
Confused about something? Feel free to DM me on discord and I would be happy to guide you through the bot's setup! `Pizerite#5648`



## How to Run and setup

There are pre-requisites you need to fulfill in order to set it up. 


1. `Discord Developer Portal` | `Bot Application` | `Bot Token` | `Enabling Intents`

Navigate to <a href="https://discord.com/developers/applications/">Discord Developer Portal</a> and login there.
You should see something like the picture below but unlike my portal page, your page should be probably empty

![image](https://user-images.githubusercontent.com/85628915/127975371-f9c7772d-91d6-453c-8ce6-f8ed385f7fca.png)

Click on the applications button in the right corner of your screen

![image](https://user-images.githubusercontent.com/85628915/127975725-02be373c-b3ba-4888-9d88-ba0670bbc2b9.png)


A window will pop up asking for name, enter the name of your bot

![image](https://user-images.githubusercontent.com/85628915/127976281-ffb5cf1a-4f87-493a-a182-fc4b50664ab7.png)



    
Now you should be directed to this page:

![image](https://user-images.githubusercontent.com/85628915/127976451-051535d9-13c9-44fa-9d12-ecbdf886d750.png)


In the settings bar, navigate to `Bot`

![image](https://user-images.githubusercontent.com/85628915/127976562-76404c6e-4ea7-40c7-b6bd-bbbc3c8c294c.png)


You should now see this page

![image](https://user-images.githubusercontent.com/85628915/127976695-dd8c90d0-a115-4e8c-8ae9-36d29bfd0c5c.png)


Click add bot and hit confirm when it asks "are you sure?"
and you should see something like this

![image](https://user-images.githubusercontent.com/85628915/127976859-32c075bc-7980-4fae-893a-f075e34a9a7a.png)

Scroll down to "Privilidged Gateway Intents" and enable both presence and member intents **(DO NOT SKIP THIS STEP!)**

![image](https://user-images.githubusercontent.com/85628915/127978500-495c1349-0b06-47c9-ae12-5865188f52d1.png)


Under the token option, click "`COPY TOKEN`"
Now, this token is a Unique token, the first part of the token is your Bot's ID converted to Base64 (before .) after dot is a securely generated main token, don't give your token to anyone, neither post it anywhere online, this gives any person who has the token the ability to control the bot, they can inject their own code and cause destruction in your server!

Go to the files you downloaded (the bot files I uploaded in the repo) and open `config.py`

In place of `YOUR_BOT_TOKEN`, paste your bot's token and save it

![image](https://user-images.githubusercontent.com/85628915/127977430-9d188ccd-27b3-4a54-84a9-161009c6a985.png)

Now go to the folder these files are in

![image](https://user-images.githubusercontent.com/85628915/127977825-a3004bfe-0821-4c70-bcae-d15a7b5c93db.png)

click the search bar and type `cmd` and hit enter

![image](https://user-images.githubusercontent.com/85628915/127977956-aec5fd75-21cb-4012-907a-dba3441c3178.png)



It should open your command prompt:

![image](https://user-images.githubusercontent.com/85628915/127978033-215e9344-c6a9-47a1-8df4-8f24d607ab47.png)

now type `python3 main.py` or `python main.py` or `py main.py` and wait for some time and you should see this

![image](https://user-images.githubusercontent.com/85628915/127978722-5c03d53b-52f3-454e-88e5-dfd5e7af22bb.png)


Congratulations! Your bot is now online :D



## Bot Assets

Now, since Emote IDs are different for every server, you can add your custom emotes manually, by default, bot will use default Discord Unicode Emojis


<p align="center">Default </p>

<img src="https://user-images.githubusercontent.com/85628915/127979412-df77d5f5-c1af-4393-9474-b07e98910096.png" align="center"><img>

<p align="center">Custom </p>

![image](https://user-images.githubusercontent.com/85628915/127979874-dcd1d4d7-82e5-4363-b6b3-07a53c1cfcd7.png)



To use these custom emotes, you need to take a short step. You will have to add these emotes in your server and replace 

Custom emotes are represented internally in the following format:
`<:name:id>`
Where the name is the name of the custom emote, and the ID is the id of the custom emote. 
For example, `<:python3:232720527448342530>` is the name:id for ![image](https://user-images.githubusercontent.com/85628915/127980329-714344af-0d37-43e0-84a3-d7db64e9b0c7.png)

You can quickly obtain the <:name:id> format by putting a backslash in front of the custom emoji when you put it in your client. 
Example: `\:python3:` would give you the `<:name:id>` format.

Animated emojis are the same as above but have an a before the name- ie: `<a:name:id>`


you need to use this "<:name:id>" in place of None in the `config.py` in respect to their correct variable names



## Bot Variables You can edit:

**DANGER_EMOTE** 

<img src="https://cdn.discordapp.com/emojis/871700064437944401.png">


**UPDATED_EMOTE**

<img src="https://cdn.discordapp.com/emojis/871699818211340328.png">

**DEFAULT_EMOTE**

<img src="https://cdn.discordapp.com/emojis/871700218419232888.png">

**EMERGENCY_EMOTE** 

<img src="https://cdn.discordapp.com/emojis/871509155054227487.png">

**SAFE_EMOTE**

<img src="https://cdn.discordapp.com/emojis/871509182136856607.png">

**ARROW_EMOTE**

<img src="https://cdn.discordapp.com/emojis/871986812816605244.png">


## A Quick Note


If you don't understand something, you can always DM me on discord `Pizerite#5648` and I would be happy to walk you through the setup of the bot on your server, even if you aren't familiar with coding!
