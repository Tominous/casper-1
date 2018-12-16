"""
Author:         David Schaeffer
Creation Date:  November 6, 2018
Purpose:        Defines all commands for the Fitness module
"""


from discord.ext import commands


class Fitness:
    def __init__(self, casper):
        self.casper = casper

    @commands.command()
    async def set(self, ctx, *, text):
        """capser set exercise:weight such as casper set bench:9000"""
        pass

    @commands.command()
    async def progress(self, ctx, user):
        """Check the current progress of someone."""
        pass

    @commands.command()
    async def checkin(self, ctx, user):
        """Use to log a day spent working out."""
        pass


def setup(casper):
    casper.add_cog(Fitness(casper))
