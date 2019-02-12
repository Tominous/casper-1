import discord
import re
import tweepy

from cogs_production.twitter.twitter_config import TwitterAPI


class Twitter:
    def __init__(self, casper):
        self.casper = casper
        auth = tweepy.OAuthHandler(TwitterAPI.API_KEY, TwitterAPI.API_SECRET)
        auth.set_access_token(TwitterAPI.ACCESS_TOKEN, TwitterAPI.ACCESS_TOKEN_SECRET)
        self.twitter = tweepy.API(auth)


def setup(casper):
    casper.add_cog(Twitter(casper))
