# Casper
Casper is a [discord](https://discordapp.com) bot written in python using the 
[discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) library. Started as a way 
to learn python, it's evolved into a great tool used by friends.

# Build Status
Casper is under near-constant development. I try to ensure only bug-free, working builds 
are uploaded here but nobody is perfect. 

# Features
Casper comes with a variety of sub-modules such as:

### Dice
- A dice parser. 
- Ex: `casper roll 2d10+6`

### Feedback
- Allows users to send feedback via the bot directly from discord.
- Ex: `casper feedback I found a bug when....`

### Fitness
- This module has a number of fitness commands allowing users to track gender, height,
weight, and their personal bests on a variety of exercises.

### Music
- Music player. This iteration is entirely thanks to [this user](https://gist.github.com/EvieePy/ab667b74e9758433b3eb806c53a19f34)
while I continue working on the intricacies to modify it to my needs.

### Reddit
- [Subreddit](https://reddit.com) linking. If Casper detects a valid subreddit in a message,
it'll reply with a link directly to that subreddit as long as it's not part of a URL.

### Reminders
- A handy reminders module. 
- Ex: `casper remindme 3 days How great is this bot?` will
result in Casper reminding you in 3 days time how great he really is.
- Allows users to add events to a countdown tracker and then view those events.
- Ex: `casper addevent 01/01/2019 New Year, New Me!`
- Ex: `casper countdown new year` will show how many days until the above event.
- Ex: `casper countdown` will show how many days until each event created by the users on
that specific discord server.

### (World of) Warcraft
- World of Warcraft character profiles and character stats. 


# Installation
You'll need to [setup your own bot credentials](https://discordapp.com/developers/applications/)
and dump them into a config.py file in the root directory. Ex:
```
class Casper:
    TOKEN = 'yourTokenString'
    CLIENT_ID = 'yourClientIDString'
    CLIENT_SECRET = 'yourClientSecretString'
```

You'll also need to add API credentials to reddit/reddit_config.py:
```
class RedditAPI:
    CLIENT_ID = 'clientID'
    CLIENT_SECRET = 'clientSecret'
    USER_PASS = 'password'
    USER_NAME = 'username'
    AUTH_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'
```

as well as warcraft/warcraft_config.py:
```
class WarcraftMedia:
    class_colors = {
        'Death Knight': 0xc41e3b, 'Demon Hunter': 0xa330c9, 'Druid': 0xff7c0a,
        'Hunter': 0xaad372, 'Mage': 0x68ccef, 'Monk': 0x00ffba, 'Paladin': 0xf48cba,
        'Priest': 0xf0ebe0, 'Rogue': 0xfff468, 'Shaman': 0x2359ff, 'Warlock': 0x9382c9,
        'Warrior': 0xc69b6d
    }
    m_plus_abbreviations_legion = {
        'brh': 'Black Rook Hold', 'coen': 'Cathedral of Eternal Night',
        'cos': 'Court of Stars', 'dht': 'Darkheart Thicket', 'eoa': 'Eye of Azshara',
        'hov': 'Halls of Valor', 'mos': 'Maw of Souls', 'nl': 'Neltharion\'s Lair',
        'upper': 'Return to Karazhan: Upper', 'lower': 'Return to Karazhan: Lower',
        'seat': 'Seat of the Triumvirate', 'arc': 'The Arcway',
        'votw': 'Vault of the Wardens'
    }
    m_plus_abbreviations_bfa = {
        'ad': 'Atal\'Dazar',
        'fh': 'Freehold',
        'kr': 'King\'s Rest',
        'ml': 'MOTHERLODE',
        'sob': 'Siege of Boralus',
        'sots': 'Shrine of the Storm',
        'tos': 'Temple of Sethrallis',
        'td': 'Tol Dagor',
        'ur': 'Underrot',
        'wm': 'Waycrest Manor'
    }
    region_codes = {
            'us': {'namespace': 'dynamic-us', 'locale': 'en_US'},
            'eu': {'namespace': 'dynamic-eu', 'locale': 'en_GB'},
            'kr': {'namespace': 'dynamic-kr', 'locale': 'ko_KR'},
            'tw': {'namespace': 'dynamic-tw', 'locale': 'zh_TW'}
        }


class BlizzardAPI:
    CLIENT_ID = 'clientID'
    CLIENT_SECRET = 'clientSecret'
    BLIZZARD_API_KEY = 'apiKey'


class WarcraftLogsAPI:
    WARCRAFTLOGS_API_KEY = 'apiKey'
```

Once done, it's just a matter of running it. `python casper.py`

# License
MIT License

Copyright (c) 2017-2018 David Schaeffer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.