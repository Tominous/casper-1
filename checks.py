from database.ban import BanMethods


class Checks:
    @staticmethod
    async def user_not_banned(ctx):
        """
        This check is run globally whenever a command is about to be invoked. If a user
        is banned, this check returns False and the command is NOT run.
        :param ctx: invocation context
        :return: False if user is banned, True otherwise
        """
        banned_users = await BanMethods.get_ban_list()
        for banned_user in banned_users:
            if ctx.author.mention == banned_user.user:
                return False
        return True
