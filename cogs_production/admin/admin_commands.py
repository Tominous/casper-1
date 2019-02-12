import asyncio
import datetime
from discord.ext import commands

from database.ban import BanMethods


class Admin:
    def __init__(self, casper):
        self.casper = casper
        self.casper.loop.create_task(self.manage_bans())

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog_dir, cog_name):
        """
        Used to load cogs currently under development to avoid rebooting casper.
        :param ctx: invocation context
        :param cog_dir: name of the directory the cog.py file is located
        :param cog_name: name of the cog.py file
        :return: A message confirming the cog loaded.
        """
        self.casper.load_extension(f'cogs_development.{cog_dir}.{cog_name}')
        return await ctx.send(f'Loaded: cogs.{cog_dir}.{cog_name}')

    @commands.command()
    @commands.is_owner()
    async def broadcast(self, ctx, *, msg: str):
        """
        This is a command to be used sparingly by the bot owner to push breaking info that
        may affect users. It will search for a single "general" chat channel on every server
        the bot belongs to and send the passed in msg param.
        :param ctx: Invoked context.
        :param msg: The message to be sent to the servers.
        :return: None
        """
        broadcast_msg_format = (
            f'**__What\'s New:__**\n\n'
            f'{msg}'
        )
        for guild in self.casper.guilds:
            for channel in guild.text_channels:
                if 'general' in channel.name:
                    await channel.send(broadcast_msg_format)
                    break  # We just want the first general chat.

    async def manage_bans(self):
        await self.casper.wait_until_ready()
        while not self.casper.is_closed():
            banned_users = await BanMethods.get_ban_list()
            for banned_user in banned_users:
                if datetime.datetime.now() > (banned_user.banned_on +
                                              datetime.timedelta(hours=banned_user.ban_time)):
                    await BanMethods.unban_user(banned_user.user)
            await asyncio.sleep(60)

    @commands.command()
    @commands.is_owner()
    async def ban(self, ctx, ban_time, user, *, reason):
        try:
            await BanMethods.ban_user(user, ctx.author.name, reason, int(ban_time))
            return await ctx.send(f'{user} has been banned for {ban_time} hours:\n'
                                  f'```{reason}```')
        except ValueError:
            return await ctx.send('Please enter ban time in hours as whole number.\n'
                                  'Example: `casper ban @user 3 user is terrible`')

    @commands.command()
    @commands.is_owner()
    async def unban(self, ctx, user):
        if await BanMethods.user_is_banned(user):
            await BanMethods.unban_user(user)
            return await ctx.send(f'{user} has been unbanned.')

    @commands.command()
    @commands.is_owner()
    async def bans(self, ctx):
        banned_users = await BanMethods.get_ban_list()
        print(banned_users)
        if banned_users:
            output = ''
            for banned_user in banned_users:
                output += (f'{banned_user.user} ({banned_user.ban_time} hours) by '
                           f'{banned_user.banned_by.title()}:\n'
                           f'{banned_user.ban_reason}\n\n')
            return await ctx.send(output)
        return await ctx.send('There are currently no banned users.')


def setup(casper):
    casper.add_cog(Admin(casper))
