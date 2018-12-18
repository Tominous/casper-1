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
        return await self.casper.process_commands(message)

    async def subreddit_check(self, message: discord.Message):
        """
        Checks incoming messages for partial subreddit names, such as /r/python. If it
        finds any possible subreddit names, it checks to see if a subreddit exists and,
        if so, creates a link for it to be sent. If a subreddit does not exist, it skips
        it.
        :param message: The discord message.
        :return: A message containing the subreddits, if any were found.
        """
        # matches /r/subredditName between other words and at newline, but not if it's
        # preceded by any other text.
        reg_exp = re.compile(r'\s(/r/+.[^ \n]*)')
        match = reg_exp.findall(message.content)  # returns list of matches
        if match:
            names = [sub.replace('/r/', '') for sub in match]
            output_str = ''
            for name in names:
                try:
                    subreddit = self.reddit.subreddits.search_by_name(name, exact=True)
                    output_str += f'<https://reddit.com/r/{name}>\n'
                except prawcore.NotFound:
                    continue
            return await message.channel.send(
                f'Found the following subreddits:\n\n{output_str}')
        return


def setup(casper):
    casper.add_cog(Reddit(casper))