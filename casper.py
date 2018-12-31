from datetime import datetime
from pathlib import Path

from discord.ext import commands

from config import Casper

bot_prefix = commands.when_mentioned_or('Casper ', 'casper ')
bot_description = """Casper is a Discord bot with a focus on character data
                  aggregation for Blizzard Entertainment franchises."""
casper = commands.Bot(command_prefix=bot_prefix, description=bot_description,
                      owner_id=Casper.OWNER_ID, pm_help=True)


@casper.event
async def on_ready():
    print('====================================\n'
          f'Started at: {datetime.now()}\n'
          f'Bot name: {casper.user.name}\n'
          f'Bot ID: {casper.user.id}\n'
          f'Owner name: {casper.get_user(casper.owner_id).name}\n'
          f'Owner ID: {casper.owner_id}\n')
    cogs_path = Path(__file__).parent / 'cogs_production'
    for sub_dir in cogs_path.iterdir():
        for cog in sub_dir.iterdir():
            # We want to make sure we're only working with cog directories,
            # not IDE settings directories.
            if 'commands' in cog.name:
                cog_name = cog.name.replace('.py', '')
                casper.load_extension(f'cogs_production.{sub_dir.name}.{cog_name}')
                print(f'Loaded: cogs.{sub_dir.name}.{cog_name}')
    print('====================================')
    return


@casper.event
async def on_member_join(member):
    """
    Whispers new members with an intro to Casper. Alerts the server to the new member
    joining.
    :param member:
    :return:
    """
    await member.send(content=f'Welcome to the {member.guild.name} discord! I\'m '
                              'Casper, a bot with a number of features available. '
                              'If you need help with any of my commands, just type '
                              '`casper help`.')
    for channel in member.guild.text_channels:
        if 'general' in channel.name:
            ch = channel
            break
    try:
        return await ch.send(f'{member.name} has joined the server.')
    except TypeError:
        # We were unable to find a "general chat"-type channel to send to.
        return


@casper.event
async def on_command(ctx):
    """
    This trigger is just for better error logging and troubleshooting.
    :param ctx:
    :return:
    """
    print(f'Command used:\n'
          f'User: {ctx.author.name}\n'
          f'Server: {ctx.guild}\n'
          f'Channel: {ctx.message.channel}\n'
          f'Command: {ctx.message.content}\n'
          f'Time: {datetime.now().time()}\n')
    return


@casper.command()
async def load(ctx, cog_dir, cog_name):
    """
    Used to load cogs currently under development to avoid rebooting casper.
    :param ctx: invocation context
    :param cog_dir: name of the directory the cog.py file is located
    :param cog_name: name of the cog.py file
    :return: A messaghe
    """
    if ctx.author.id == casper.owner_id:
        casper.load_extension(f'cogs_development.{cog_dir}.{cog_name}')
        return await ctx.send(f'Loaded: cogs.{cog_dir}.{cog_name}')


@casper.command()
async def broadcast(ctx, *, msg: str):
    if ctx.author.id == casper.owner_id:
        broadcast_msg_format = (
            f'**__What\'s New:__**\n\n'
            f'{msg}'
        )
        for guild in casper.guilds:
            for channel in guild.text_channels:
                if 'general' in channel.name:
                    await channel.send(broadcast_msg_format)
                    break  # We just want the first general chat.


if __name__ == '__main__':
    casper.run(Casper.TOKEN)
