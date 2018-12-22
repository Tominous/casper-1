"""
Author:         David Schaeffer
Creation Date:  December 22, 2018
Purpose:        Defines all commands for the Feedback module
"""

from datetime import datetime
from discord.ext import commands


class Feedback:
    def __init__(self, casper):
        self.casper = casper

    @commands.command()
    async def feedback(self, ctx, *, text):
        """
        Allows a user to send feedback directly to me via discord.
        """
        dev_account = self.casper.get_user(self.casper.owner_id)
        formatted_message = (
            f'==========================================================\n'
            f'New feedback from **{ctx.author.name}** received on {datetime.now()}\n\n'
            f'{text}\n'
            f'==========================================================\n'
        )
        return await dev_account.send(formatted_message)


def setup(casper):
    casper.add_cog(Feedback(casper))
