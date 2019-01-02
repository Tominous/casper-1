"""
Author:         David Schaeffer
Creation Date:  December 13, 2018
Purpose:        Defines all commands for the Reminder module
"""
import re

import discord
import praw
import prawcore

from cogs_production.reddit.reddit_config import RedditAPI


class Reddit:
    def __init__(self, casper):
        self.casper = casper
        self.reddit = praw.Reddit(client_id=RedditAPI.CLIENT_ID,
                                  client_secret=RedditAPI.CLIENT_SECRET,
                                  password=RedditAPI.USER_PASS,
                                  user_agent='casper_bot by /u/dave_schaeffer',
                                  username=RedditAPI.USER_NAME)

    async def on_message(self, message):
        if message.author == self.casper.user:
            return
        await self.subreddit_check(message)

    async def subreddit_check(self, message: discord.Message):
        """
        Checks incoming messages for partial subreddit names, such as r/python. If it
        finds any possible subreddit names, it checks to see if a subreddit exists and,
        if so, creates a link for it to be sent. If a subreddit does not exist, it skips
        it.
        :param message: The discord message.
        :return: A message containing the subreddits, if any were found.
        """
        # matches /r/subredditName between other words and at newline but not if it's
        # part of a URL
        reg_exp = re.compile(r'((?<!.com/)r/[a-zA-Z_]+(?![a-zA-Z0-9/]))')
        match = reg_exp.findall(message.content)  # returns list of matches
        if match:
            names = [sub.replace('r/', '') for sub in match]
            output_str = ''
            for name in names:
                try:
                    # If we don't get the NotFound error, it's a valid subreddit.
                    subreddit = self.reddit.subreddits.search_by_name(name, exact=True)
                    output_str += f'<https://old.reddit.com/r/{name}>\n'
                except prawcore.NotFound:
                    # Invalid subreddit, skip to next name in list.
                    output_str += f'"{name}" is not a subreddit.'
            return await message.channel.send(
                f'{output_str}')
        return


def setup(casper):
    casper.add_cog(Reddit(casper))
