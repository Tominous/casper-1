from discord.ext import commands

from database.ban import BanMethods


class Checks:
    @staticmethod
    async def user_not_banned(ctx):
        banned_users = await BanMethods.get_ban_list()
        for banned_user in banned_users:
            if ctx.author.mention == banned_user.user:
                return False
        return True
