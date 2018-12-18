# Casper
Casper is a [discord](https://discordapp.com) bot written in python using the 
[discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) library. Started as a way 
to learn python, it's evolved into a great tool used by friends.

# Build Status
Casper is under near-constant development. I try to ensure only bug-free, working builds 
are uploaded here but nobody is perfect. 

# Features
Casper comes with a variety of sub-modules such as:

- A dice parser. Ex: `casper roll 2d10+6`
- A handy reminders module. Ex: `casper remindme 3 days How great is this bot?` will
result in Casper reminding you in 3 days time how great he really is.
- Video game account profiles. If an online game you play offers an API to retrieve game
data, Casper can be used to aggregate that data into user-friendly outputs right into
discord chat. 
- [Subreddit](https://reddit.com) linking. If Casper detects a valid subreddit in a message,
it'll reply with a link directly to that subreddit.

# Installation
You'll need to [setup your own bot credentials](https://discordapp.com/developers/applications/)
and dump them into a config.py file in the root directory. Ex:
```
class Casper:
    TOKEN = 'yourTokenString'
    CLIENT_ID = 'yourClientIDString'
    CLIENT_SECRET = 'yourClientSecretString'
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